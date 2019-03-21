from kafka import KafkaConsumer
import json

try:
    print('Welcome to parse engine')
    consumer = KafkaConsumer('test-topic', bootstrap_servers=['kafka:29092'])
    for message in consumer:
        print('im a message')
        print(message)
        
except Exception as e:
    print(e)
    # Logs the error appropriately. 
    pass