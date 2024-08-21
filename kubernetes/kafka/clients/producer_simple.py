from confluent_kafka import Producer
import socket

conf = {
    'bootstrap.servers': '127.0.0.1:63401',  # Correct external bootstrap server address
    'client.id': socket.gethostname()
}

producer = Producer(conf)

def delivery_report(err, msg):
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))

topic = 'demo-topic'  # Define your topic name here

for i in range(10):
    producer.produce(topic, key=str(i), value='Hello Kafka {}'.format(i), callback=delivery_report)
    producer.flush()

print("Messages sent successfully")
