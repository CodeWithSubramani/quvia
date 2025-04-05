import asyncio
import json
import os
import random
from datetime import datetime, timedelta
from typing import Dict, Any

from confluent_kafka import Producer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer
from confluent_kafka.serialization import SerializationContext, MessageField
from dotenv import load_dotenv

# Configuration
load_dotenv()
KAFKA_BROKER = os.getenv('KAFKA_BROKER', "localhost:29092")
SCHEMA_REGISTRY_URL = os.getenv('SCHEMA_REGISTRY_URL', "http://localhost:8081")
TOPIC_NAME = "flight_positions"

# Schema Registry Client
schema_registry_conf = {'url': SCHEMA_REGISTRY_URL}
schema_registry_client = SchemaRegistryClient(schema_registry_conf)

# Avro Schema
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
        print(f"❌ Delivery failed: {err}")
    else:
        print(f"✅ Delivered to {msg.topic()} [{msg.partition()}] @ offset {msg.offset()}")


def generate_random_hex() -> str:
    return ''.join(random.choices('0123456789ABCDEF', k=6))


def generate_random_callsign() -> str:
    airline = random.choice(
        ['THY892', 'KLM892', 'BAW892', 'SAS892', 'RYR892', 'AAR892', 'MEA892', 'SEH892', 'HYS892', 'FDB892'])
    return f"{airline}"


def generate_random_flight_data() -> Dict[str, Any]:
    now = datetime.now() + timedelta(hours=5, minutes=30)
    has_hex = random.random() > 0.1  # 90% chance to have hex
    has_callsign = random.random() > 0.1  # 90% chance to have callsign

    lat = random.uniform(45.0, 50.0)
    lon = random.uniform(14.0, 22.0)

    flight = {
        "fr24_id": ''.join(random.choices('0123456789abcdef', k=8)),
        "hex": generate_random_hex() if has_hex else None,
        "callsign": generate_random_callsign() if has_callsign else None,
        "lat": round(lat, 5),
        "lon": round(lon, 5),
        "track": random.randint(0, 359),
        "alt": random.choice([38000, 39000, 40000, 41000]),
        "gspeed": random.randint(260, 500),
        "vspeed": random.choice([-64, -32, 0, 32, 64]),
        "squawk": ''.join(random.choices('01234567', k=4)),
        "timestamp": (now - timedelta(seconds=random.randint(0, 60))).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source": random.choice(["ADSB", "MLAT"])
    }
    return flight


def transform_flight_data(flight_data: Dict[str, Any]) -> Dict[str, Any]:
    """Transform flight data to match Avro schema"""
    return {
        "flight_id": flight_data.get('fr24_id'),
        "hex": flight_data.get('hex'),
        "callsign": flight_data.get('callsign'),
        "latitude": flight_data.get('lat'),
        "longitude": flight_data.get('lon'),
        "track": float(flight_data.get('track')),
        "altitude": float(flight_data.get('alt')),
        "gspeed": float(flight_data.get('gspeed')),
        "vspeed": float(flight_data.get('vspeed')),
        "squawk": flight_data.get('squawk'),
        "timestamp": int(datetime.strptime(flight_data['timestamp'], "%Y-%m-%dT%H:%M:%SZ").timestamp() * 1000),
        "source": flight_data.get('source')
    }


def produce_flight_data(flight_data: Dict[str, Any]):
    """Produce flight data to Kafka"""
    try:
        transformed_data = transform_flight_data(flight_data)
        serialized_data = avro_serializer(transformed_data, SerializationContext(TOPIC_NAME, MessageField.VALUE))
        producer.produce(
            topic=TOPIC_NAME,
            value=serialized_data,
            callback=delivery_report
        )
        producer.poll(0)
    except Exception as e:
        print(f"Error producing message: {e}")


async def generate_and_produce_flights():
    """Generate random flight data and produce to Kafka"""
    print(f"Starting flight data producer at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("Press Ctrl+C to stop...")

    try:
        while True:
            # Generate a batch of flights
            flights = [generate_random_flight_data() for _ in range(random.randint(3, 8))]
            print(f"Generated {len(flights)} flights")

            # Produce each flight
            for flight in flights:
                produce_flight_data(flight)

            # Flush and wait
            producer.flush()
            await asyncio.sleep(1)

    except KeyboardInterrupt:
        print("\nStopping producer...")
    finally:
        producer.flush()
        print("Producer stopped")


if __name__ == "__main__":
    try:
        asyncio.run(generate_and_produce_flights())
    except KeyboardInterrupt:
        print("\nScript stopped by user")
