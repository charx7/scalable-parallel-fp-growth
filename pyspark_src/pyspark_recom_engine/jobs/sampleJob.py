from pyspark_recom_engine.spark import get_spark, test_import
from pyspark_recom_engine.utils.dataframeUdfs import list_sorter
from pyspark_recom_engine.fpGrowth.fpGrowthAlgo import CreateTree, mainMerge
from pyspark_recom_engine.fpGrowth.fpGrowthLastSteps import find_values, generatePowerset, generate_association_rules
# Own imports
#from pyspark_recom_engine import list_sorter
import json
import pprint
#import pandas as pd
import time
from pyspark.sql import SparkSession, SQLContext
from pyspark.sql.dataframe import DataFrame
from pyspark.sql.types import IntegerType, ArrayType, StringType, MapType
from pyspark.sql import functions as F
from pyspark.sql.functions import udf, array


def main():
    '''
        Sample Spark job to test if everything is ok!
    '''
    # Simple test stuff to write to the db
    # print("Writing to the mongodb")
    # test_data = [(1, "alice"), (2, "gustavo")]
    # test_headers = ["_id", "name"]
    # test_df = spark_session.createDataFrame(test_data, test_headers)
    # test_df.write.format("com.mongodb.spark.sql.DefaultSource").mode("append").save()

    # # Test read from the db
    # print('reading form the mongodb')
    # mongo_data = spark_session.read \
    # .format("com.mongodb.spark.sql.DefaultSource") \
    # .option("database", "testdb") \
    # .option("collection", "myColl") \
    # .load()

    # print("The generated schema of the mongo is: \n")
    # mongo_data.printSchema()
    # print("The first row of the collection is: \n")
    # mongo_data.show()

    ###################################################
    # Test read from the transactions restored db
    print("Reading from transactions db... \n")
    transactions_data = spark_session.read \
        .format("com.mongodb.spark.sql.DefaultSource") \
        .option("database", "transactions") \
        .option("collection", "transactions") \
        .load()

    print("The generated transactions schema is: \n")
    transactions_data.printSchema()
    print("The show data is: \n")
    transactions_data.show()
    print("Showing the column of product code lists")
    transactions_data.select("ProductCode").show()

    # transactions_data.createOrReplaceTempView("transactions")
    select_transactions = transactions_data.select("ProductCode")

    # size of using a build in func
    transactions_data.withColumn("no_of_transactions", F.size("ProductCode"))

    # Use udf to define a row-at-a-time udf
    countTransactions = udf(lambda x: len(x), IntegerType())
    # Apply the function
    transactions_with_count = transactions_data.select(
        'TransactionID',
        'ProductCode',
        countTransactions('ProductCode').alias('no_of_transactions2')
    )

    # Explode the transactions list (will generate a column for each item in a transaction)
    exploded_transactions = transactions_with_count.select(
        'TransactionID',
        'ProductCode',
        'no_of_transactions2',
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
    # Map step to the resulting dataframe CreateTree(x) with arbitraty key 1 (all must be reduced?)
    testPrint = sorted_data.select(
        'OrderedProductCode').rdd.map(lambda x: CreateTree(x))

    end = time.time()
    print('Time Elapsed: ', end - start)
    print('######### End Map phase ###############')
    # Unconmment to print
    # add .take(20) at the end of testPrint to collect partials (this transforms them to a list)
    # index = 0
    # for text in testPrint:
    #     print('Index is: ', index)
    #     print(text, '\n')
    #     index = index + 1
    # Reduce step of the algo
    print('########## Start Reduce phase ##########')
    start = time.time()
    fpTree = testPrint.reduce(lambda x, y: mainMerge(x, y))
    end = time.time()
    print('Time Elapsed: ', end - start)
    print('########## Finished Reducing ###########')

    #print('The type is: ', type(fpTree))
    print('The merged fp-tree is: ', fpTree)
    fpTree.display()

    print('Making a dict out of the tree...')
    jsonifiedFpTree = json.dumps(fpTree.makeDictionary())

    # Ugly spark concatenation
    filtered_odered_freqs_concat = filtered_odered_freqs_percent.withColumn(
        'item_freq',
        F.concat(
            F.lit('("'),
            F.col('individual_items'),
            F.lit('",'),
            F.col('count'),
            F.lit(')')
        ).alias('concatenated_item_freq')
    )
    print('DF to Mine using the grown fp-tree is: ')
    filtered_odered_freqs_concat.show()

    # Use udf to define a row-at-a-time udf
    generateCondPattern = udf(lambda x: find_values(
        str(x), jsonifiedFpTree), ArrayType(StringType()))
    # Apply the function
    conditional_patterns = filtered_odered_freqs_concat.select(
        'individual_items',
        'count',
        'percentage',
        generateCondPattern('individual_items').alias('conditional_patterns')
    )
    print('\nThe generated conditional patterns are: ')
    conditional_patterns.show()

    # Use a UDF to generate the subsets of a given item on the item support table
    generateSubset = udf(lambda x: generatePowerset(
        x[0], x[1], threshold_value), ArrayType(MapType(StringType(), StringType())))
    # Apply the function
    items_subset = conditional_patterns.select(
        'individual_items',
        'conditional_patterns',
        'count',
        generateSubset(
            array(F.col('individual_items').cast(StringType()), F.col('conditional_patterns'
                                                                      ).cast(StringType()))).alias('conditional_patterns_set')
    )
    print('\nThe subsets generated after mining the tree are: ')
    items_subset.show()

    # Debug stuff
    debug = items_subset.select('conditional_patterns_set').take(2)
    print('The subsets are: ', debug)

    exploded_items_subset = items_subset.select(
        F.explode_outer('conditional_patterns_set').alias('items')
    )
    print('The exploded transactions data is: \n')
    exploded_items_subset.show()  # Show in the console

    # Collect the first list to pass the rule generating func
    collected_exploded_items_subset = exploded_items_subset.select(
        'items').collect()
    first_collectedList = [
        row.items for row in collected_exploded_items_subset if row.items != None]
    # Pretty print
    pprint.pprint(first_collectedList)

    # Collect the second list to pass the rule generating func
    collected_exploded_single_item_freq = filtered_odered_freqs_concat.select(
        'item_freq').collect()
    second_collectedList = [
        row.item_freq for row in collected_exploded_single_item_freq]
    # Pretty print
    pprint.pprint(second_collectedList)

    # Rules generation
    # threshold
    final_output = generate_association_rules(
        first_collectedList, second_collectedList, 0.1)
    print('The generated rules are: \n')
    pprint.pprint(final_output)

    # # Collect
    # collectedRowsData = filtered_odered_freqs_concat.select('item_freq').collect()
    # # Convert into list
    # collectedList = [row.item_freq for row in collectedRowsData]
    # # Tuple em
    # tupledCollectedList = [eval(x) for x in collectedList]
    # print(tupledCollectedList)
    # # ankits pandas stuff
    # itemSupportTable = pd.DataFrame(tupledCollectedList,columns=['item','support'])
    # conditionalPatternBaseTable = generateConditionalPatternBase(itemSupportTable,jsonifiedFpTree)

    # print(conditionalPatternBaseTable)
    # # Debug shit
    # for index in range(conditionalPatternBaseTable.shape[0]):
    #     print('\n Conditional Patterns for item: ', \
    #         conditionalPatternBaseTable.iloc[index]['item'], \
    #         ' are: \n')
    #     for item in conditionalPatternBaseTable.iloc[index]['ConditionalPattern']:
    #         print(item)


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
