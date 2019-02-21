# Example Package

This is a simple example package. You can use
[Github-flavored Markdown](https://guides.github.com/features/mastering-markdown/)
to write your content.

This will be the main entrypoint pont of the spark project, ie dockerfiles should be here

## Build the Spark-Master
build docker master image on spark_master 
```
docker build -t spark-master ./spark_master/ 
```
Run the docker images of the spark-master
```
sudo docker run --rm  --name spark-master -p 4040:4040 -p 8080:8080 -p 7077:7077 -h spark-master -e ENABLE_INIT_DAEMON=false -d spark-master

```

## Build the Spark-Slaves
Build the slaves image
```
sudo docker build --rm -t bde/spark-app ./pyspark_src/
```

Run the image that has the job specified on the Dockerfile
```
sudo docker run --rm --name spark-worker-1 --link spark-master:spark-master -e ENABLE_INIT_DAEMON=false -d bde/spark-app #sleep 10000 command when docker is being a rebel

```
