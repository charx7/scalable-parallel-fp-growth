# Extend the spark python template dockerimage
FROM bde2020/spark-worker:2.4.0-hadoop2.7

# Copy the requirements.txt first, for separate dependency resolving and downloading
# the -p is to make it recursive
RUN mkdir -p /app
COPY requirements.txt /app/
RUN cd /app \
    && pip3 install -r requirements.txt

# Configure the following environment variables (unless the default value satisfies):
ENV SPARK_MASTER_NAME "spark-master"
ENV SPARK_MASTER_PORT "7077"

#### Commands for the submit image ####
#ENV SPARK_APPLICATION_ARGS