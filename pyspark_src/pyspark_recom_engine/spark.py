# Pyspark imports
from pyspark.sql import SparkSession
from functools import lru_cache
from pyspark import SparkContext, SparkConf

# Spark session builder
# The get_spark() function is memoized using @lru_cache decorator
@lru_cache(maxsize=None)
def get_spark():
    conf = SparkConf().setAppName("recomEngineApp")
    sc = SparkContext(conf=conf)
    return (
        sc
    )
