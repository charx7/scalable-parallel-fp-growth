help:
	@echo "start-cluster - Will start an spark-master with a single slave"
	@echo "build-docker  - Will build the docker images on your systems with the required params"
	@echo "start-cluster - Will run the built docker containers"
	@echo "submit-app    - Will submit the python prebuilt app into the cluster"
	@echo "clean-cluster - Will stop and remove the containers from your system"
	
build-docker:
	@echo "Building the docker images..."
	@docker build -t spark-master ./spark_master/
	@docker build --rm -t bde/spark-app ./pyspark_worker/
	@docker build --rm -t submit-pyspark-job ./pyspark_src/

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

submit-app:
	@echo "Submiting app into the cluster"
	@docker run --rm --name pyspark-app -e ENABLE_INIT_DAEMON=false --link spark-master:spark-master -d submit-pyspark-job sleep 10000

clean-cluster:
	@echo "Removing images..."
	@docker stop spark-master
	@docker stop spark-worker-1
	@docker stop pyspark-app
	@docker ps -a