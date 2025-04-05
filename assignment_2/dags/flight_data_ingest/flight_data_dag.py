import time
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator
from flight_data_ingest.producer import Flightradar24API, transform_flight_data, produce_flight_data, producer

default_args = {
    'owner': 'airflow',
    'retries': 3,  # Increased retries for more resilience
    'retry_delay': timedelta(seconds=30),  # Shorter delay between retries
    'depends_on_past': False,
    'email_on_failure': True,
    'email_on_retry': False,
}


def run_producer():
    fr24 = Flightradar24API()
    while True:  # Continuous loop for perpetual operation
        try:
            api_data = fr24.fetch_flight_data()
            if api_data:
                flights = transform_flight_data(api_data)
                for flight in flights:
                    produce_flight_data(flight)
                producer.flush()
            time.sleep(10)  # Short delay between fetches to avoid rate limiting
        except Exception as e:
            # Log error and continue unless it's a critical exception
            print(f"Error occurred: {str(e)}")
            time.sleep(30)  # Longer delay after error
            continue


with DAG(
        dag_id='flight_data_to_kafka_streaming',
        default_args=default_args,
        start_date=datetime(2024, 1, 1),
        schedule_interval=None,  # Set to None as we'll trigger once and let it run
        catchup=False,
        max_active_runs=1,  # Ensure only one instance runs at a time
        description='Continuously ingest live flight data and stream to Kafka'
) as dag:
    task = PythonOperator(
        task_id='stream_flight_data_to_kafka',
        python_callable=run_producer,
        execution_timeout=None,  # Remove timeout to allow perpetual running
        do_xcom_push=False
    )
