import subprocess
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.email import send_email

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}


def check_and_restart():
    container_name = "assignment_2-flight-producer-1"
    result = subprocess.run(
        ["docker", "inspect", "-f", "{{.State.Running}}", container_name],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    status = result.stdout.decode().strip()

    if status != "true":
        print(f"{container_name} is not running. Restarting...")
        subprocess.run(["docker", "restart", container_name])

        send_email(
            to=["subramani0595@gmail.com"],  # Replace with your email
            subject="Flight Producer Restarted",
            html_content=f"{container_name} was down and has been restarted by Airflow."
        )
    else:
        print(f"{container_name} is running.")


with DAG(
        dag_id='monitor_flight_producer',
        default_args=default_args,
        start_date=datetime(2024, 1, 1),
        schedule_interval='*/1 * * * *',  # Run every 2 minutes
        catchup=False
) as dag:
    # notify_start = EmailOperator(
    #     task_id='notify_dag_start',
    #     to='subramani0595@gmail.com',  # Replace with your email
    #     subject='Flight Producer DAG Started',
    #     html_content='The Flight Producer DAG has started.'
    # )

    monitor_task = PythonOperator(
        task_id='check_and_restart_flight_producer',
        python_callable=check_and_restart
    )
# notify_start >> monitor_task
monitor_task
