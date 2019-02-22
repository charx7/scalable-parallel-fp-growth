# Product Recomendation Engine

This will be the main entrypoint pont of the spark project, ie dockerfiles should be here

## Build the Spark-Master
build docker master image on spark_master 
```
docker build -t spark-master ./spark_master/ 
```
Run the docker images of the spark-master
```
docker run --rm  --name spark-master -p 4040:4040 -p 8080:8080 -p 7077:7077 -h spark-master -e ENABLE_INIT_DAEMON=false -d spark-master

```

## Build the Spark-Slaves
Build the slaves image
```
docker build --rm -t bde/spark-app ./pyspark_worker/
```

Run the image that has the job specified on the Dockerfile
```
docker run --rm --name spark-worker-1 -p 8081:8081 --link spark-master:spark-master -e ENABLE_INIT_DAEMON=false -d bde/spark-app #sleep 10000 command when docker is being a rebel
```

## Submit a Pyspark Job
After build and run of Spark Master -> Slaves
Build the submit container
```
docker build --rm -t submit-pyspark-job ./pyspark_src/
```
Run the submit container
```

```

## Alternative
Build the docker cluster using the Makefil
```
make build-docker
```
Run the containers if you have already built the docker images
```
make start-cluster
```
Remove them just by stopping the containers (they are removed automatically)
```
make clean-cluster
```

TODO: 
- Define a network instead of a --link
- Get everything set-up in a composer -> Kubernetes for the cloud?
- Get conditionals that accept shell/bash commands on the Makefile