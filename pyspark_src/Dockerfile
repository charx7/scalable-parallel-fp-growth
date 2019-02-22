# Will extend form the spark-template that extends on itself with the spark-submit image
FROM bde2020/spark-python-template:2.4.0-hadoop2.7

# Needed params
ENV SPARK_MASTER_NAME "spark-master"
ENV SPARK_MASTER_PORT "7077"
# Not sure if will work with this (this should be built by a parent image!)
ENV SPARK_MASTER_URL "spark://spark-master:7077"
# Should be this or directly the python egg?
ENV SPARK_APPLICATION_PYTHON_LOCATION app/pyspark_recom_engine/jobs/sampleJob.py
# Extra (Maybe will be needed after?)
ENV SPARK_APPLICATION_ARGS "foo bar baz"
# Add the python egg for inter-package dependancies 
ENV SPARK_SUBMIT_ARGS="--py-files app/dist/pyspark_recom_engine-0.1-py3.6.egg"

CMD ["/submit.sh"]