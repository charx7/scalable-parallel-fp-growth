# Will extend form the spark-template that extends on itself with the spark-submit image
#FROM bde2020/spark-python-template:2.4.0-hadoop2.7
# Using an image b4 (the one that has the python reqs install)
FROM bde2020/spark-submit:2.4.0-hadoop2.7 

COPY template.sh /

# Install the C libraries because pandas/pysparkml needs to compile C code
#ARG PANDAS_VERSION=0.24.1
RUN apk add --no-cache python3-dev libstdc++ && \
    apk add --no-cache --virtual .build-deps g++ && \
    apk add --no-cache --update gcc musl-dev libffi-dev openssl-dev && \
    apk add build-base && \
    ln -s /usr/include/locale.h /usr/include/xlocale.h && \
    pip3 install numpy==1.15.1 && \
    pip3 install cython && \
    apk del .build-deps

# Copy the requirements.txt first, for separate dependency resolving and downloading
COPY requirements.txt /app/
#RUN pip3 install --upgrade pip
RUN cd /app \
      && pip3 install -r requirements.txt

# Copy the source code
COPY . /app

# Needed params
ENV SPARK_MASTER_NAME "spark-master"
ENV SPARK_MASTER_PORT "7077"
# Not sure if will work with this (this should be built by a parent image!)
ENV SPARK_MASTER_URL "spark://spark-master:7077"
# Should be this or directly the python egg?
ENV SPARK_APPLICATION_PYTHON_LOCATION app/pyspark_recom_engine/jobs/SparkLibraryJob.py
# Extra (Maybe will be needed after?)
ENV SPARK_APPLICATION_ARGS "foo bar baz"
# Add the python egg for inter-package dependancies 
# on the --packages flag we add spark dependancies that otherwise would be built by sbt
ENV SPARK_SUBMIT_ARGS="--packages org.mongodb.spark:mongo-spark-connector_2.11:2.4.0 --py-files app/dist/pyspark_recom_engine-0.1-py3.6.egg"

CMD ["/bin/bash","/template.sh","/submit.sh"]