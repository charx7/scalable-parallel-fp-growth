# Pyspark imports
from pyspark.sql import SparkSession
from functools import lru_cache

# Spark session builder
# The get_spark() function is memoized using @lru_cache decorator
@lru_cache(maxsize=None)
def get_spark():
    return (SparkSession.builder
                .master("local")
                .appName("gill")
                .getOrCreate())
