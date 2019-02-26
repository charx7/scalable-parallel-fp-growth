help:
	@echo "start-cluster - Will start an spark-master with a single slave"
	@echo "build-docker  - Will build the docker images on your systems with the required params"
	@echo "start-cluster - Will run the built docker containers"
	@echo "submit-app    - Will submit the python prebuilt app into the cluster"
	@echo "clean-cluster - Will stop and remove the containers from your system"
	@echo "package-pyspark-app: - Will package a python egg to submit into spark"
	@echo "start-mongo:  - Will start a mongodb container with a volume on ./data/"

# Here the $(shell ) tag is needed to execute shell comands
start-mongo:
	@echo "Creating the mongo container..."
	@docker run --rm --name spark-mongo -p 27017:27017 --link spark-master:spark-master -v $(shell pwd)/data:/data/db/ -d mongo

build-docker:
	@echo "Building the docker images..."
	@docker build -t spark-master ./spark_master/
	@docker build --rm -t bde/spark-app ./pyspark_worker/

start-cluster:
	@echo "Starting the Spark Cluster..."
	# @if [ ! "$(docker ps -q -f name=spark-masterrr)" ] ; then\
	# 	echo "An instance of Spark-master is already running" ;\
	# fi
	@docker run --rm  --name spark-master -p 4040:4040 -p 8080:8080 -p 7077:7077 -h spark-master -e ENABLE_INIT_DAEMON=false -d spark-master
	@docker run --rm --name spark-worker-1 -p 8081:8081 --link spark-master:spark-master -e ENABLE_INIT_DAEMON=false -d bde/spark-app
	@docker ps -a
	@echo "Sucess opening spark master on your browser"
	# We need the sleep in order wait for the slave to connect to the master
	@sleep 2
	@xdg-open http://localhost:8080

package-pyspark-app:
	@echo "Packaging the python egg to be submitted alongside the job..."
	@(cd ./pyspark_src && python setup.py bdist_egg)

submit-app:
	@echo "Package python app -> Built Docker Image -> Run the Submit container"
	make package-pyspark-app
	@echo "Submiting app into the cluster"
	@docker build --rm -t submit-pyspark-job ./pyspark_src/
	@echo "Image built, now running the submit container" 
	@docker run --rm --name pyspark-app -e ENABLE_INIT_DAEMON=false --link spark-master:spark-master -d submit-pyspark-job 

clean-cluster:
	@echo "Removing containers..."
	@docker stop spark-master
	@docker stop spark-worker-1
	@docker stop pyspark-app
	@docker ps -a