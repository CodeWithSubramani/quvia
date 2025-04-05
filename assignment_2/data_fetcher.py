import json
import os
import time
from datetime import datetime

import requests
from dotenv import load_dotenv


class Flightradar24API:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv('API_KEY')
        self.base_url = "https://fr24api.flightradar24.com/api/live/flight-positions/light"
        self.headers = {
            'Accept-Version': 'v1',
            "Accept": "application/json",
            'Authorization': f'Bearer {self.api_key}'

        }
        self.last_request_time = 0
        self.min_request_interval = 10  # seconds (to respect rate limits)

    def fetch_flight_data(self):
        """
        Fetch real-time flight data from the Flightradar24 API.

        Returns:
            dict: Flight data if successful, None otherwise
        """
        # Ensure we respect rate limits
        time_since_last_request = time.time() - self.last_request_time
        if time_since_last_request < self.min_request_interval:
            wait_time = self.min_request_interval - time_since_last_request
            print(f"Waiting {wait_time:.1f} seconds to respect rate limits...")
            time.sleep(wait_time)

        try:
            params = {
                'bounds': '50.682,46.218,14.422,22.243'
            }

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
                print(f"Response: {response.text}")
                return None

        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return None

    def save_to_file(self, data, filename_prefix="flight_data"):
        """
        Save flight data to a JSON file with a timestamp.

        Args:
            data (dict): Flight data to save
            filename_prefix (str): Prefix for the output file
        """
        if not data:
            return

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{filename_prefix}_{timestamp}.json"

        with open(os.path.join('data', filename), 'w') as f:
            json.dump(data, f, indent=2)

        print(f"Data saved to {filename}")


def main():
    fr24 = Flightradar24API()

    fetch_interval = 10

    print(f"Starting Flightradar24 data fetcher (interval: {fetch_interval} seconds)")
    print("Press Ctrl+C to stop...")

    try:
        while True:
            print(f"\nFetching data at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

            # Fetch flight data
            flight_data = fr24.fetch_flight_data()

            if flight_data:
                # Print some basic info
                if 'result' in flight_data and 'response' in flight_data['result']:
                    num_flights = len(flight_data['result']['response']['data'])
                    print(f"Received data for {num_flights} flights")

                # Save to file
                fr24.save_to_file(flight_data)
            else:
                print("No data received or error occurred")

            # Wait for the next interval
            time.sleep(fetch_interval)

    except KeyboardInterrupt:
        print("\nScript stopped by user")


if __name__ == "__main__":
    main()
