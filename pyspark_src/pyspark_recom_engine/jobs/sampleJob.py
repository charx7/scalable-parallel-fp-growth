from pyspark_recom_engine.spark import get_spark, test_import
from pyspark_recom_engine.utils.dataframeUdfs import list_sorter
from pyspark_recom_engine.fpGrowth.fpGrowthAlgo import CreateTree
# Own imports
#from pyspark_recom_engine import list_sorter

from pyspark.sql import SparkSession, SQLContext
from pyspark.sql.dataframe import DataFrame
from pyspark.sql.types import IntegerType, ArrayType, StringType
from pyspark.sql import functions as F 
from pyspark.sql.functions import udf
 
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
        .option("collection", "transcations") \
        .load()

    print("The generated transactions schema is: \n")
    transactions_data.printSchema()
    print("The show data is: \n")
    transactions_data.show()
    print("Showing the column of product code lists")
    transactions_data.select("ProductCode").show()

    #transactions_data.createOrReplaceTempView("transactions")
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
    exploded_transactions.show() # Show in the console

    exploded_transactions_group = exploded_transactions.select("*").groupBy(
        'individual_items'
    ).count()

    ordered_freqs = exploded_transactions_group.orderBy(
        exploded_transactions_group['count'].desc()
    )
    ordered_freqs.show() # Show method

    # Now we divide by the original count 
    noOfTransactions = transactions_data.count() # Total count of the original data
    # Divide the freqs by the noOfTransactions column
    ordered_freqs_percents = ordered_freqs.withColumn(
        'percentage',
        ordered_freqs['count'] / float(noOfTransactions)
    )
    # # How many transactions are above 1%?
    threshold = 0.001
    filtered_odered_freqs_percent = ordered_freqs_percents \
        .select("*") \
        .filter(
        ordered_freqs_percents['percentage'] > threshold
    )
    filtered_odered_freqs_percent.show() # Show
    filtered_count = filtered_odered_freqs_percent.count()
    print('\nThe number of item frequency above ', threshold\
        ,'is: ', filtered_count, '\n')
    
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
    sortTransactions = udf(lambda x: list_sorter(x, orderedItemsDict), ArrayType(StringType()))
    # Apply the function
    sorted_data = transactions_data.select(
        'TransactionID',
        sortTransactions('ProductCode').alias('OrderedProductCode')
    ).na.drop()
    sorted_data.show()

    testPrint = sorted_data.select('OrderedProductCode').rdd.map(lambda x: (CreateTree(x),1)).take(20)
    
    index = 0
    for json in testPrint:
        print('Index is: ', index)
        print(json, '\n')
        index = index + 1

if __name__ == '__main__':
    # There is a bug that doesnt pass spark session objects when called from another func    
    spark_session = SparkSession.builder \
        .appName("recomEngine") \
        .config("spark.mongodb.input.uri", "mongodb://spark-mongo:27017/testdb.myColl") \
        .config("spark.mongodb.output.uri", "mongodb://spark-mongo:27017/testdb.myColl") \
        .config('spark.jars.packages', "org.mongodb.spark:mongo-spark-connector_2.11:2.4.0") \
        .getOrCreate()
    spark_session.sparkContext.setLogLevel("ERROR") # Set log level to error
    # Execute main method
    main()