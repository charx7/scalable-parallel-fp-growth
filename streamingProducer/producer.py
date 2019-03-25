from kafka import KafkaProducer
import pymongo
import pprint
from pymongo import MongoClient
from bson.json_util import dumps
import time

while(True):
    # Open connection to db
    client = MongoClient('mongodb://spark-mongo:27017/')
    db = client['transactions']

    # Read random transactions from db
    data = db.transactions.aggregate(
        [
            {
                '$sample': {'size': 3}
            }
        ]
    )
    # Produce sample message from localhost
    # producer = KafkaProducer(bootstrap_servers=['localhost:9092'], retries=5)
    # Produce message from docker
    producer = KafkaProducer(bootstrap_servers=['kafka:29092'], retries=5)

    producer.send('test-topic', dumps(data).encode('utf-8'))

    # block until all async messages are sent
    producer.flush()
    # tidy up the producer connection
    producer.close()
    time.sleep(10)
