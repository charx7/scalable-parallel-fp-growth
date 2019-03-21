help:
	@echo "start-cluster - Will start an spark-master with a single slave"
	@echo "build-docker  - Will build the docker images on your systems with the required params"
	@echo "start-cluster - Will run the built docker containers"
	@echo "submit-app    - Will submit the python prebuilt app into the cluster"
	@echo "clean-cluster - Will stop and remove the containers from your system"
	@echo "package-pyspark-app: - Will package a python egg to submit into spark"
	@echo "start-mongo:  - Will start a mongodb container with a volume on ./data/"
	@echo "stream-data:  - Will start the (producer) streamer container that sends data to kafka"

# Here the $(shell ) tag is needed to execute shell comands
start-mongo:
	@echo "Creating the mongo container..."
	@docker run --rm --name spark-mongo -p 27017:27017 --network spark-network --link spark-master:spark-master -v $(shell pwd)/data:/data/db/ -d mongo

build-docker:
	@echo "Building the docker images..."
	@docker build -t spark-master ./spark_master/
	@docker build --rm -t bde/spark-app ./pyspark_worker/

start-cluster:
	@echo "Creating Network..."
	@docker network create spark-network
	@echo "Starting the Spark Cluster..."
	@docker run --rm  --name spark-master -p 4040:4040 -p 8080:8080 -p 7077:7077 --network spark-network -h spark-master -e ENABLE_INIT_DAEMON=false -d spark-master
	@docker run --rm --name spark-worker-1 -p 8081:8081 --network spark-network -e ENABLE_INIT_DAEMON=false -d bde/spark-app
	make start-mongo
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
	@docker run --rm --name pyspark-app -e ENABLE_INIT_DAEMON=false -p 4040:4040 --network spark-network submit-pyspark-job

clean-cluster:
	@echo "Removing containers..."
	@docker stop spark-master
	@docker stop spark-worker-1
	@docker stop spark-mongo
	@echo "Removing the network..."
	@docker network rm spark-network
	@docker ps -a

stream-data:
	@echo "Streaming data from the streamingProducer container"
	@echo "Add sleep 60000 to debug the container"
	@docker build --rm -t python-streamer ./streamingProducer
	@docker run --rm --name producer-container --network spark-network python-streamer
	