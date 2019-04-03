#!/bin/bash

. "/spark/sbin/spark-config.sh"

. "/spark/bin/load-spark-env.sh"

mkdir -p $SPARK_WORKER_LOG

export SPARK_HOME=/spark

ln -sf /dev/stdout $SPARK_WORKER_LOG/spark-worker.out

# Toggle to debug a greater sleep, some sleep is needed to give time to the master 
sleep 20

# Execute the connection to the master
/spark/sbin/../bin/spark-class org.apache.spark.deploy.worker.Worker \
 --webui-port $SPARK_WORKER_WEBUI_PORT $SPARK_MASTER \
 --memory 1G --cores 1  >> $SPARK_WORKER_LOG/spark-worker.out

