from kafka import KafkaProducer

# Produce sample message
producer = KafkaProducer(bootstrap_servers=['localhost:9092'], retries=5)
producer.send('test-topic', b'from local python')
print("Published msg -> 'super-duper-message' on Topic -> 'messages'")
# block until all async messages are sent
producer.flush()
# tidy up the producer connection
producer.close()
