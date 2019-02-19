#from pyspark_recom_engine.spark import get_spark
from pyspark.sql import SparkSession

def main():
    '''
        Sample Spark job to test if everything is ok!
    '''
    spark = (SparkSession.builder
                .master("local")
                .appName("recom-engine")
                .getOrCreate())

    #spark = get_spark()
    sc = spark.sparkContext
    rdd = sc.parallelize([1,2,3,4,5,6,7])
    
    print('The count is: ',rdd.count())

if __name__ == '__main__':
    main()