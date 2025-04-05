from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator

from producer import Flightradar24API, transform_flight_data, produce_flight_data, producer

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}


def run_producer():
    fr24 = Flightradar24API()
    api_data = fr24.fetch_flight_data()
    if api_data:
        flights = transform_flight_data(api_data)
        for flight in flights:
            produce_flight_data(flight)
        producer.flush()


with DAG(
        dag_id='flight_data_to_kafka',
        default_args=default_args,
        start_date=datetime(2024, 1, 1),
        schedule_interval='@hourly',
        catchup=False
) as dag:
    task = PythonOperator(
        task_id='fetch_and_produce_flight_data',
        python_callable=run_producer
    )
