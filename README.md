# Product Recomendation Engine

This will be the main entrypoint pont of the spark project, ie dockerfiles should be here

## Simple Build with Docker Compose

The easiest way to run the project is to run the cluster with docker compose.

```
docker-compose up
```

Afterwards, you need to make sure the data is inside of the
mongo volume if you haven't done so. There are two volumes, mongodb and mongodb_config.
The data should be inside of the mongodb volume.

Then, submit the application from the pyspark src.

```
make submit-app
```

## Build the Spark-Master

build docker master image on spark_master

```
docker build -t spark-master ./spark_master/
```

Run the docker images of the spark-master

```
docker run --rm  --name spark-master -p 4040:4040 -p 8080:8080 -p 7077:7077 -h spark-master -e ENABLE_INIT_DAEMON=false -d spark-master

```

## Run the mongodb container

Run the mongo db inside a container where spark will read our data

```
docker run --rm --name spark-mongo -p 27017:27017 --link spark-master:spark-master -v $(pwd)/data:/data/db/ -d mongo
```

To execute the mongo shell inside the container:

```
docker exec -it spark-mongo /bin/bash
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
docker run --rm --name pyspark-app -e ENABLE_INIT_DAEMON=false --link spark-master:spark-master -d submit-pyspark-job sleep 10000

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

## Restore db dump inside mongo container

How to restore the Database inside the mongo container

- Create a folder inside the mongo docker container volume where you wish to copy the data to restore "transcations.bson" and "transcations.metadata.json"

```
docker exec -it {YOUR_DIRECTORY_NAME}_spark-mongo_1 /bin/bash
cd data
mkdir restore
```

- Navigate to the directory where you have the db dump and copy both files from your computer to the docker volume via docker cp

```
docker cp transcations.bson {YOUR_DIRECTORY_NAME}_spark-mongo_1:/data/restore
docker cp transcations.metadata.json {YOUR_DIRECTORY_NAME}_spark-mongo_1:/data/restore
```

- Inside the mongo docker container run the mongo restore command at the data restore directory

```
docker exec -it {YOUR_DIRECTORY_NAME}_spark-mongo_1 /bin/bash
cd data/restore
# -d is the name of the database to create/replace
# --drop is necessary if you are replacing an existing db
# . is the directory where your backup files are located
mongorestore --drop -d transactions .
```

- Verify that the db has been restored using the mongo shell.
