from kafka import KafkaConsumer
import json

try:
    print('Welcome to parse engine')
    # From inside a container
    #consumer = KafkaConsumer('test-topic', bootstrap_servers='kafka:29092')
    # From localhost
    consumer = KafkaConsumer('test-topic', bootstrap_servers='localhost:9092', auto_offset_reset='earliest')
    for message in consumer:
        print('im a message')
        print(message)
        
except Exception as e:
    print(e)
    # Logs the error appropriately. 
    pass