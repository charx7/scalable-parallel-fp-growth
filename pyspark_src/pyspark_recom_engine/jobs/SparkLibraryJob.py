import json
import pprint
import os
#import pandas as pd
import time
from pyspark.sql import SparkSession, SQLContext
from pyspark.sql.dataframe import DataFrame
from pyspark.sql.types import IntegerType, ArrayType, StringType, MapType
from pyspark.sql import functions as F
from pyspark.sql.functions import udf, array

from pyspark.ml.fpm import FPGrowth

def main():
    # Read from the transactions database and transactions collection, this will
    # generate a Dataframe object
    print("Reading from transactions db... \n")
    transactions_data = spark_session.read \
        .format("com.mongodb.spark.sql.DefaultSource") \
        .option("database", "transactions") \
        .option("collection", "transactions") \
        .load()
    print('Our read transactions are of the type: ',type(transactions_data), '\n')

    print("The generated transactions schema is: \n")
    transactions_data.printSchema()
    print("The data fetched from the dbb is: \n")
    transactions_data.show()
    
    product_codes = transactions_data.select("ProductCode")
    fpGrowth = FPGrowth(itemsCol="ProductCode",
                        minSupport=0.0001, minConfidence=0.05)
    
    print('Fitting the model...')
    model = fpGrowth.fit(product_codes)

    # Display frequent itemsets.
    model.freqItemsets.show()

    # Display generated association rules.
    model.associationRules.show(100)

    # transform examines the input items against all the association rules and summarize the
    # consequents as prediction
    model.transform(transactions_data).show()

    # Simple test stuff to write to the db
    print("Writing to the mongodb")
    model.associationRules.write.format(
        "com.mongodb.spark.sql.DefaultSource") \
        .option("database", "transactions") \
        .option("collection", "recommendations") \
        .mode("append") \
        .save()

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
