#from pyspark_recom_engine.spark import get_spark
from pyspark.sql import SparkSession, SQLContext

def main():
    '''
        Sample Spark job to test if everything is ok!
    '''
    # Simple test stuff to write to the db
    print("Writing to the mongodb")
    test_data = [(1, "alice"), (2, "gustavo")]
    test_headers = ["_id", "name"]
    test_df = spark_session.createDataFrame(test_data, test_headers)
    test_df.write.format("com.mongodb.spark.sql.DefaultSource").mode("append").save()

    # Test read from the db
    print('reading form the mongodb')
    mongo_data = spark_session.read \
    .format("com.mongodb.spark.sql.DefaultSource") \
    .option("database", "testdb") \
    .option("collection", "myColl") \
    .load()

    print("The generated schema of the mongo is: \n")
    mongo_data.printSchema()
    print("The first row of the collection is: \n")
    mongo_data.show()

if __name__ == '__main__':
    # There is a bug that doesnt pass spark session objects when called from another func    
    spark_session = SparkSession.builder \
        .appName("recomEngine") \
        .config("spark.mongodb.input.uri", "mongodb://spark-mongo:27017/testdb.myColl") \
        .config("spark.mongodb.output.uri", "mongodb://spark-mongo:27017/testdb.myColl") \
        .config('spark.jars.packages', "org.mongodb.spark:mongo-spark-connector_2.11:2.4.0") \
        .getOrCreate()

    main()