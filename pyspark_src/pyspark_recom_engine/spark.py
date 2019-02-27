# Pyspark imports
from pyspark.sql import SparkSession, SQLContext
from functools import lru_cache
#from pyspark import SparkContext, SparkConf

# Spark session builder
# The get_spark() function is memoized using @lru_cache decorator
@lru_cache(maxsize=None)
def get_spark():
    # conf = SparkConf().setAppName("recomEngineApp")
    # sc = SparkContext(conf=conf)
    spark_session = SparkSession.builder \
        .appName("recomEngine") \
        .config("spark.mongodb.input.uri", "mongodb://mongo:27017/testdb.myCol") \
        .config("spark.mongodb.output.uri", "mongodb://mongo:27017/testdb.myCol") \
        .getOrCreate()

    print('Spark Session Created')
    return (
        spark_session
    )
