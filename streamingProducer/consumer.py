""" Read test data from Kafka to ensure producer and broker are working """
import json

from kafka import KafkaConsumer

# To consume latest messages and auto-commit offsets
consumer = KafkaConsumer('test-topic',
                        #  group_id='test-consumer',
                        #  bootstrap_servers='localhost:9092',
                        #api_version=(0, 10, 1)
                         )

for message in consumer:
    # message value and key are raw bytes -- decode if necessary!
    # e.g., for unicode: `message.value.decode('utf-8')`
    print(message)
