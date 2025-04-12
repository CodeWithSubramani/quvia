import json
import os
from datetime import datetime

import requests
import sseclient
from confluent_kafka import Producer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer
from confluent_kafka.serialization import SerializationContext, MessageField
from dotenv import load_dotenv

# Load env
load_dotenv()
KAFKA_BROKER = os.getenv('KAFKA_BROKER', "kafka:9092")
producer_conf = {'bootstrap.servers': KAFKA_BROKER, 'log_level': 7, 'acks': 'all',
                 'retries': 3, }
producer = Producer(producer_conf)

SCHEMA_REGISTRY_URL = os.getenv('SCHEMA_REGISTRY_URL', "http://schema-registry:8081")
TOPIC_NAME = "flight_positions"

# Schema
avro_schema = {
    "type": "record",
    "name": "FlightPosition",
    "namespace": "com.flight.analytics",
    "fields": [
        {"name": "flight_id", "type": "string"},
        {"name": "hex", "type": ["null", "string"], "default": None},
        {"name": "callsign", "type": ["null", "string"], "default": None},
        {"name": "latitude", "type": "double"},
        {"name": "longitude", "type": "double"},
        {"name": "track", "type": "float"},
        {"name": "altitude", "type": "float"},
        {"name": "gspeed", "type": "float"},
        {"name": "vspeed", "type": "float"},
        {"name": "squawk", "type": ["null", "string"], "default": None},
        {"name": "timestamp", "type": "long"},
        {"name": "source", "type": ["null", "string"], "default": None}
    ]
}
avro_schema_str = json.dumps(avro_schema)

# Schema registry
schema_registry_conf = {'url': SCHEMA_REGISTRY_URL}
schema_registry_client = SchemaRegistryClient(schema_registry_conf)

# Serializer
avro_serializer = AvroSerializer(schema_registry_client, avro_schema_str, lambda o, c: o)


def kafka_error_cb(err):
    print(f"Kafka error: {err}")


def delivery_report(err, msg):
    if err:
        print(f"❌ Delivery failed: {err}")
    else:
        print(f"✅ Delivered to {msg.topic()} [{msg.partition()}] @ offset {msg.offset()}")


def transform(data):
    print(data)
    try:
        # Check if the timestamp is a string and convert it to an integer
        if isinstance(data["timestamp"], str):
            data["timestamp"] = int(datetime.strptime(data["timestamp"], "%Y-%m-%dT%H:%M:%SZ").timestamp() * 1000)
        elif not isinstance(data["timestamp"], int):
            raise ValueError(f"Invalid timestamp format: {data['timestamp']}")

        data["flight_id"] = data.pop("fr24_id", data.get("flight_id"))  # Handle both `fr24_id` and `flight_id`
        data["latitude"] = float(data.pop("lat", data.get("latitude")))
        data["longitude"] = float(data.pop("lon", data.get("longitude")))
        data["altitude"] = float(data.pop("alt", data.get("altitude")))
        data["track"] = float(data.get("track", 0))  # Default to 0 if missing
        data["gspeed"] = float(data.get("gspeed", 0))  # Default to 0 if missing
        data["vspeed"] = float(data.get("vspeed", 0))  # Default to 0 if missing
        return data
    except (ValueError, KeyError, TypeError) as e:
        raise ValueError(f"Invalid data format: {data}, error: {e}")


def produce(data):
    try:
        if isinstance(data, list):  # Check if data is a list
            for item in data:  # Process each item in the list
                transformed = transform(item)
                serialized = avro_serializer(transformed, SerializationContext(TOPIC_NAME, MessageField.VALUE))
                print('server event serialized:', serialized)
                producer.produce(TOPIC_NAME, value=serialized, callback=delivery_report)
        elif isinstance(data, dict):  # If it's a single dictionary, process it directly
            transformed = transform(data)
            serialized = avro_serializer(transformed, SerializationContext(TOPIC_NAME, MessageField.VALUE))
            print('server event serialized:', serialized)
            producer.produce(TOPIC_NAME, value=serialized, callback=delivery_report)

        else:
            print(f"❌ Unexpected data format: {data}")

        # Increase polling timeout for better processing
        producer.poll(1)  # Make sure we allow more time for delivery reports
        producer.flush()  # Forcefully flush the producer to ensure delivery
    except Exception as e:
        print(f"Error producing message: {e}")


def main():
    print("Connecting to SSE stream...")
    response = requests.get("http://flight-mock-service:8000/stream", stream=True)
    client = sseclient.SSEClient(response)

    for event in client.events():
        try:
            data = json.loads(event.data)
            produce(data)
        except Exception as e:
            print(f"❌ Failed to handle event: {e}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n🛑 Stopped by user")
    finally:
        producer.flush()
