from pyspark_recom_engine.spark import get_spark
from pyspark.sql import SparkSession, SQLContext
#from pyspark import SparkContext, SparkConf

def main():
    '''
        Sample Spark job to test if everything is ok!
    '''

    # Get the session
    spark = get_spark()
    l = [('Alice', 1)]
    print('The context object is: ')
    print(spark)
    
    df = spark.createDataFrame(l).collect()

if __name__ == '__main__':
    main()