# Spark-sql imports
import pyspark.sql.functions as F

# This just appends life_goal column to a dataset
def with_life_goal(df):
    return df.withColumn("life_goal", F.lit("escape!"))
