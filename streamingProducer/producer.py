from kafka import KafkaProducer

# Produce sample message from localhost
#producer = KafkaProducer(bootstrap_servers=['localhost:9092'], retries=5)
# Produce sample message ffrom docker
producer = KafkaProducer(bootstrap_servers=['kafka:29092'], retries=5)

producer.send('test-topic', b'from docker python')
print("Published msg -> 'from docker python' on Topic -> 'test-topic'")
# block until all async messages are sent
producer.flush()
# tidy up the producer connection
producer.close()
