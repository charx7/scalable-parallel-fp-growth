FROM bde2020/spark-base:2.4.0-hadoop2.7

COPY worker.sh /

ENV SPARK_WORKER_WEBUI_PORT 8081
ENV SPARK_WORKER_LOG /spark/logs
ENV SPARK_MASTER "spark://spark-master:7077"

EXPOSE 8081

# Copy the requirements.txt first, for separate dependency resolving and downloading
# the -p is to make it recursive
RUN mkdir -p /app
COPY requirements.txt /app/
RUN cd /app \
    && pip3 install -r requirements.txt

# Configure the following environment variables (unless the default value satisfies):
ENV SPARK_MASTER_NAME "spark-master"
ENV SPARK_MASTER_PORT "7077"

CMD ["/bin/bash", "/worker.sh"]
