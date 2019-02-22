# Will extend form the spark-template that extends on itself with the spark-submit image
FROM bde2020/spark-python-template:2.4.0-hadoop2.7

# Needed params
ENV SPARK_MASTER_NAME "spark-master"
ENV SPARK_MASTER_PORT 7077
ENV SPARK_APPLICATION_PYTHON_LOCATION app/pyspark_recom_engine/jobs/sampleJob.py
# Extra (Maybe will be needed after?)
ENV SPARK_APPLICATION_ARGS "foo bar baz"

CMD ["/bin/bash"]