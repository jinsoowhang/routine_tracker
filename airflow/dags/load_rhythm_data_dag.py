from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(
    dag_id="load_raw_rhythm_data",
    start_date=datetime(2023, 1, 1),
    schedule_interval="@daily",
    catchup=False,
) as dag:

    # Task to run the Python script
    load_data = BashOperator(
        task_id="load_data",
        bash_command="python3 /opt/airflow/main.py --user=root --password=root --host=pg-database --port=5432 --db=rhythm",
    )

    # Task to run DBT
    run_dbt = BashOperator(
        task_id="run_dbt",
        bash_command="cd /opt/airflow/dbt && dbt run",
    )

    # Set task dependencies (first run load_data, then run_dbt)
    load_data >> run_dbt