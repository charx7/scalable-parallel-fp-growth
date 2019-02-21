help:
	@echo "start-cluster - will start an spark-master with a single slave"

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

clean-cluster:
	@echo "Removing images..."
	@docker stop spark-master
	@docker stop spark-worker-1
