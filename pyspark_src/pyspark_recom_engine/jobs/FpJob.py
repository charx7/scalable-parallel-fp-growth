# Own imports
from pyspark_recom_engine.spark import get_spark, test_import
from pyspark_recom_engine.utils.dataframeUdfs import list_sorter
from pyspark_recom_engine.fpGrowth.fpGrowthParallel import mapTransactions, getConditionalItems, generateRules

import json
import pprint
import time
from pyspark.sql import SparkSession, SQLContext
from pyspark.sql.dataframe import DataFrame
from pyspark.sql.types import IntegerType, ArrayType, StringType, MapType
from pyspark.sql import functions as F
from pyspark.sql.functions import udf, array

def main():
    '''
        Fp growth job according to the paper.
    '''
    # Read from the transactions restored db
    print("Reading from transactions db... \n")
    transactions_data = spark_session.read \
        .format("com.mongodb.spark.sql.DefaultSource") \
        .option("database", "transactions") \
        .option("collection", "transactions") \
        .load()

    print("The generated transactions schema is: \n")
    transactions_data.printSchema()

    print("The data from the dbb is: \n")
    transactions_data.show()
    
    # Use an udf to define a row-at-a-time udf
    countTransactions = udf(lambda x: len(x), IntegerType())
    # Apply the function
    transactions_with_count = transactions_data.select(
        'TransactionID',
        'ProductCode',
        countTransactions('ProductCode').alias('no_of_transactions')
    )

    # Explode the transactions list (will generate a column for each item in a transaction)
    exploded_transactions = transactions_with_count.select(
        'TransactionID',
        'ProductCode',
        'no_of_transactions',
        F.explode_outer('ProductCode').alias('individual_items')
    )
    print('The exploded transactions data is: \n')
    exploded_transactions.show()  # Show in the console

    exploded_transactions_group = exploded_transactions.select("*").groupBy(
        'individual_items'
    ).count()

    ordered_freqs = exploded_transactions_group.orderBy(
        exploded_transactions_group['count'].desc()
    )
    print('The Grouped by item exploded transactions data counted and ordered by freq is: \n')
    ordered_freqs.show()  # Show method

    # Now we divide by the original count
    noOfTransactions = transactions_data.count()  # Total count of the original data
    # Divide the freqs by the noOfTransactions column
    ordered_freqs_percents = ordered_freqs.withColumn(
        'percentage',
        ordered_freqs['count'] / float(noOfTransactions)
    )
    # # How many transactions are above 1%?
    threshold = 0.0002
    filtered_odered_freqs_percent = ordered_freqs_percents \
        .select("*") \
        .filter(
            ordered_freqs_percents['percentage'] > threshold
        )
    print('The filtered freqs data above the threshold is: \n')
    filtered_odered_freqs_percent.show()  # Show
    filtered_odered_freqs_percent.select("count")
    threshold_row = filtered_odered_freqs_percent.agg(
        {'count': 'min'}).collect()[0]
    threshold_value = threshold_row['min(count)']
    filtered_count = filtered_odered_freqs_percent.count()
    print('\nThe number of item frequency above ',
          threshold, 'is: ', filtered_count, '\n')

    # Collect the result: transform into rdd -> flatMap -> collect()
    orderedItemsList = filtered_odered_freqs_percent.select(
        'individual_items'
    ).rdd.flatMap(lambda x: x).collect()
    #print('\n The item list is: ', orderedItemsList)

    # Make a dict using the orderedItemsList
    orderedItemsIndex = [item for item in range(len(orderedItemsList))]
    # Make a dictionary using zip
    orderedItemsDict = dict(zip(orderedItemsList, orderedItemsIndex))

    # Use udf to define a row-at-a-time udf
    sortTransactions = udf(lambda x: list_sorter(
        x, orderedItemsDict), ArrayType(StringType()))
    # Apply the function
    sorted_data = transactions_data.select(
        'TransactionID',
        sortTransactions('ProductCode').alias('OrderedProductCode')
    ).na.drop()

    print('Filtered ordered (original) transactions (according to relevance threshold)')
    sorted_data.show()

    print('######### Start Map phase #############')
    start = time.time()
    
    # Process the header table
    header_table = {}
    for k in orderedItemsDict.keys():
        header_table[str(k)] = orderedItemsDict[k]
    
    # Map step to the resulting dataframe 
    flattenedMappedProducts = sorted_data.select(
        'OrderedProductCode').rdd \
            .flatMap(lambda x: mapTransactions(header_table,x.OrderedProductCode)) 

    print('The flattened Mapped products rdd is: ', flattenedMappedProducts.take(20))

    end = time.time()
    print('Time Elapsed: ', end - start)
    print('######### End Map phase ###############')

    print('######### Start Reduce phase #############')
    start = time.time()
    # Intersection method
    reducedProducts = flattenedMappedProducts.reduceByKey(lambda x, y: x + y)
    print('The reduced products rdd is: ', reducedProducts.take(1))

    # Get conditional items (fp-tree)
    countThreshold = round(threshold * noOfTransactions)
    conditionalPatterns = reducedProducts.map(lambda x: getConditionalItems(x, countThreshold))
    print('The conditional patterns rdd is: ', conditionalPatterns.take(20))

    end = time.time()
    print('Time Elapsed: ', end - start)
    print('######### End Reduce phase ###############')
    
    # pretty print the conditional patterns
    #pprint.pprint(conditionalPatterns.take(700))

    # Collect the second list to pass the rule generating func
    collected_item_support_table_names = filtered_odered_freqs_percent.select(
        'individual_items').collect()
    collected_item_support_table_freqs = filtered_odered_freqs_percent.select(
        'count').alias('freqs').collect()
    collectedItemSupportTableNames = [
            row.individual_items for row in collected_item_support_table_names
        ]
    collectedItemSupportTableFreqs = [
        row.asDict()['count'] for row in collected_item_support_table_freqs
    ]
    itemSupportTable = dict(zip(collectedItemSupportTableNames, collectedItemSupportTableFreqs))
    # Pretty print
    print('The first element of the collected item support table is: key ',
     next(iter(itemSupportTable)), ' with value: ', itemSupportTable[next(iter(itemSupportTable))])
    
    
    # Rule generation mapper
    print('######### Start Second Map phase #############')
    start = time.time()
    # Get the rules from a given conditional pattern
    rules = conditionalPatterns.flatMap(lambda x: generateRules(itemSupportTable, x, header_table, 0.05))

    end = time.time()
    print('Time Elapsed: ', end - start)
    print('######### End Second Map phase ###############')

    # Show records
    filtered_rules = rules.filter(lambda x: x != {})

    # Convert into a df for writing to the db
    rules_df = filtered_rules.toDF(['bought-item(s)','confidence','suggested-item(s)'])
    rules_df.show()

    print("Writing to the mongodb...")
    rules_df.write.format(
        "com.mongodb.spark.sql.DefaultSource") \
        .option("database", "transactions") \
        .option("collection", "recommendations") \
        .mode("overwrite") \
        .save()
    print("\nSucces writing to the mongodb!")
    #time.sleep(1000000)
    #For debug
    #result = filtered_rules.collect()
    #pprint.pprint(result)
    # rulesList = rules.collect()
    # rules_no_empty = [ record for record in rulesList if len(record)>0]
    # #print(itemSupportTable)
    # pprint.pprint(rules_no_empty)


if __name__ == '__main__':
    # There is a bug that doesnt pass spark session objects when called from another func
    spark_session = SparkSession.builder \
        .appName("recomEngine") \
        .config("spark.mongodb.input.uri", "mongodb://spark-mongo:27017/testdb.myColl") \
        .config("spark.mongodb.output.uri", "mongodb://spark-mongo:27017/testdb.myColl") \
        .config('spark.jars.packages', "org.mongodb.spark:mongo-spark-connector_2.11:2.4.0") \
        .getOrCreate()
    spark_session.sparkContext.setLogLevel("ERROR")  # Set log level to error
    # Execute main method
    main()
