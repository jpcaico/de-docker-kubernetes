from kafka import KafkaConsumer

consumer = KafkaConsumer(
    'events',
    bootstrap_servers='localhost:29092',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    value_deserializer=lambda x: x.decode('utf-8')
)

for message in consumer:
    print(f"Key: {message.key}, Value: {message.value}, Offset: {message.offset}")
