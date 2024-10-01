from kafka import KafkaProducer, KafkaConsumer
import json

def create_producer(bootstrap_servers):
    return KafkaProducer(bootstrap_servers=bootstrap_servers, value_serializer=lambda v: json.dumps(v).encode('utf-8'))

def create_consumer(bootstrap_servers, topic):
    print("Creez consumatorul!!!")
    return KafkaConsumer(topic, bootstrap_servers=bootstrap_servers, value_deserializer=lambda m: json.loads(m.decode('utf-8')))