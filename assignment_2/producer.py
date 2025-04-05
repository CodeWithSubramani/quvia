import json
import time
from datetime import datetime

from confluent_kafka import Producer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer
from confluent_kafka.serialization import SerializationContext, MessageField

# Configuration
KAFKA_BROKER = "localhost:29092"
SCHEMA_REGISTRY_URL = "http://localhost:8081"
TOPIC_NAME = "flight_positions"

# Schema Registry Client
schema_registry_conf = {'url': SCHEMA_REGISTRY_URL}
schema_registry_client = SchemaRegistryClient(schema_registry_conf)

# Avro Schema (same as above)
avro_schema = {
    "type": "record",
    "name": "FlightPosition",
    "namespace": "com.flight.analytics",
    "fields": [
        {"name": "flight_id", "type": "string"},
        {"name": "callsign", "type": ["null", "string"], "default": None},
        {"name": "latitude", "type": "double"},
        {"name": "longitude", "type": "double"},
        {"name": "altitude", "type": "float"},
        {"name": "speed", "type": "float"},
        {"name": "heading", "type": "float"},
        {"name": "vertical_rate", "type": ["null", "float"], "default": None},
        {"name": "timestamp", "type": "long"},
        {"name": "origin", "type": ["null", "string"], "default": None},
        {"name": "destination", "type": ["null", "string"], "default": None},
        {"name": "squawk", "type": ["null", "string"], "default": None}
    ]
}

avro_schema_str = json.dumps(avro_schema)

# Avro Serializer
avro_serializer = AvroSerializer(schema_registry_client,
                                 avro_schema_str,
                                 lambda obj, ctx: obj)

# Kafka Producer Configuration
producer_conf = {
    'bootstrap.servers': KAFKA_BROKER,
}

producer = Producer(producer_conf)


def delivery_report(err, msg):
    """Callback for message delivery reports"""
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")


def produce_flight_data(flight_data):
    """Produce flight data to Kafka"""
    try:
        # Serialize the flight data
        serialized_data = avro_serializer(flight_data, SerializationContext(TOPIC_NAME, MessageField.VALUE))

        # Produce to Kafka
        producer.produce(topic=TOPIC_NAME,
                         value=serialized_data,
                         callback=delivery_report)

        producer.poll(0)
    except Exception as e:
        print(f"Error producing message: {e}")


def fetch_and_produce_flight_data():
    sample_flight = {
        "flight_id": "abc123",
        "callsign": "DAL123",
        "latitude": 37.7749,
        "longitude": -122.4194,
        "altitude": 3500.5,
        "speed": 245.6,
        "heading": 123.4,
        "vertical_rate": 12.3,
        "timestamp": int(datetime.now().timestamp() * 1000),
        "origin": "SFO",
        "destination": "JFK",
        "squawk": "1234"
    }

    produce_flight_data(sample_flight)


if __name__ == "__main__":
    while True:
        fetch_and_produce_flight_data()
        time.sleep(1)
