# Extend the spark python template dockerimage
FROM bde2020/spark-worker:2.4.0-hadoop2.7

# Configure the following environment variables (unless the default value satisfies):
ENV     SPARK_MASTER_NAME "spark-master"
ENV     SPARK_MASTER_PORT "7077"
#     SPARK_APPLICATION_ARGS

# On this case change the python entrypoint
ENV SPARK_APPLICATION_PYTHON_LOCATION /pyspark_recom_engine/jobs/sampleJob.py
# Dunno Lol
ENV SPARK_APPLICATION_ARGS "foo bar baz"
