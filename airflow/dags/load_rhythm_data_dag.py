from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(
    dag_id="load_raw_rhythm_data",
    start_date=datetime(2023, 1, 1),
    schedule_interval="@daily",
    catchup=False,
) as dag:

    load_data = BashOperator(
    task_id="load_data",
    bash_command="pip install -r /opt/airflow/requirements.txt && python3 /opt/airflow/main.py --user=root --password=root --host=pg-database --port=5432 --db=rhythm || echo 'Python script failed'",
    )