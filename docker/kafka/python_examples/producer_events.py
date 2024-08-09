from kafka import KafkaProducer
import random
import time

producer = KafkaProducer(bootstrap_servers='localhost:29092')

for x in range(10):
    n = random.random()
    producer.send('events', key=b"Key %d" % x, value=b"Message %f" % n)
    time.sleep(1)  # Add a delay to avoid flooding the broker

producer.flush()  # Ensure all messages are sent
producer.close()