# Pyspark imports
from pyspark.sql import SparkSession
from functools import lru_cache

# The get_spark() function is memoized using @lru_cache decorator
#@lru_cache(maxsize=None)
def get_spark():
    print("Creating Spark session!")
    return( 
        SparkSession.builder.appName("recomEngine").config("spark.mongodb.input.uri", "mongodb://mongo:27017/testdb.myCol").config("spark.mongodb.output.uri", "mongodb://mongo:27017/testdb.myCol").getOrCreate()
    )

def test_import():
    print('test')
    