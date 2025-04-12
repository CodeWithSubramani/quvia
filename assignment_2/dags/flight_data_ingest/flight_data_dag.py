import subprocess
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}


def check_and_restart():
    container_name = "flight-producer"
    # Check if container is running
    result = subprocess.run(
        ["docker", "inspect", "-f", "{{.State.Running}}", container_name],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    status = result.stdout.decode().strip()

    if status != "true":
        print(f"{container_name} is not running. Restarting...")
        subprocess.run(["docker", "restart", container_name])
    else:
        print(f"{container_name} is running.")


with DAG(
        dag_id='monitor_flight_producer',
        default_args=default_args,
        start_date=datetime(2024, 1, 1),
        schedule_interval='*/2 * * * *',  # Run every 2 minutes
        catchup=False
) as dag:
    monitor_task = PythonOperator(
        task_id='check_and_restart_flight_producer',
        python_callable=check_and_restart
    )
