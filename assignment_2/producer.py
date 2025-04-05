import json
import os
import time
from datetime import datetime

import requests
from confluent_kafka import Producer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer
from confluent_kafka.serialization import SerializationContext, MessageField
from dotenv import load_dotenv

# Configuration
load_dotenv()
KAFKA_BROKER = "localhost:29092"
SCHEMA_REGISTRY_URL = "http://localhost:8081"
TOPIC_NAME = "flight_positions"
API_KEY = os.getenv('API_KEY')

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


class Flightradar24API:
    def __init__(self):
        self.base_url = "https://fr24api.flightradar24.com/api/live/flight-positions/light"
        self.headers = {
            'Accept-Version': 'v1',
            "Accept": "application/json",
            'Authorization': f'Bearer {API_KEY}'
        }
        self.last_request_time = 0
        self.min_request_interval = 10  # seconds (to respect rate limits)

    def fetch_flight_data(self):
        """Fetch real-time flight data from the Flightradar24 API."""
        # Ensure we respect rate limits
        time_since_last_request = time.time() - self.last_request_time
        if time_since_last_request < self.min_request_interval:
            wait_time = self.min_request_interval - time_since_last_request
            print(f"Waiting {wait_time:.1f} seconds to respect rate limits...")
            time.sleep(wait_time)

        try:
            params = {'bounds': '50.682,46.218,14.422,22.243'}
            response = requests.get(
                self.base_url,
                headers=self.headers,
                params=params,
                timeout=10
            )

            self.last_request_time = time.time()

            if response.status_code == 200:
                return response.json()
            elif response.status_code == 429:
                print("Rate limit exceeded. Waiting before retrying...")
                time.sleep(60)  # Wait a minute if rate limited
                return None
            else:
                print(f"API request failed with status code {response.status_code}")
                return None

        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return None


def delivery_report(err, msg):
    """Callback for message delivery reports"""
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")


def produce_flight_data(flight_data):
    """Produce flight data to Kafka"""
    try:
        serialized_data = avro_serializer(flight_data, SerializationContext(TOPIC_NAME, MessageField.VALUE))
        producer.produce(
            topic=TOPIC_NAME,
            value=serialized_data,
            callback=delivery_report
        )
        producer.poll(0)
    except Exception as e:
        print(f"Error producing message: {e}")


def transform_flight_data(api_data):
    """Transform API response data to match our Avro schema"""
    if not api_data:
        return []

    flights = []
    for flight in api_data['data']:
        transformed = {
            "flight_id": flight.get('fr24_id'),
            "hex": flight.get('hex'),
            "callsign": flight.get('callsign'),
            "latitude": flight.get('lat'),
            "longitude": flight.get('lon'),
            "track": flight.get('track'),
            "altitude": float(flight.get('alt')),
            "gspeed": float(flight.get('gspeed')),
            "vspeed": float(flight.get('vspeed')),
            "squawk": flight.get('squawk'),
            "timestamp": int(datetime.strptime(flight['timestamp'], "%Y-%m-%dT%H:%M:%SZ").timestamp() * 1000),
            "source": flight.get('squawk')
        }
        flights.append(transformed)

    return flights


def main():
    fr24 = Flightradar24API()
    fetch_interval = 10  # seconds

    print(f"Starting Flightradar24 data fetcher (interval: {fetch_interval} seconds)")
    print("Press Ctrl+C to stop...")

    try:
        while True:
            print(f"\nFetching data at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

            # Fetch flight data
            api_data = fr24.fetch_flight_data()

            if api_data:
                # Transform and produce each flight
                flights = transform_flight_data(api_data)
                print(f"Processing {len(flights)} flights...")

                for flight in flights:
                    produce_flight_data(flight)

                # Flush producer to ensure all messages are sent
                producer.flush()

            # Wait for the next interval
            time.sleep(fetch_interval)

    except KeyboardInterrupt:
        print("\nScript stopped by user")
        producer.flush()


if __name__ == "__main__":
    main()
