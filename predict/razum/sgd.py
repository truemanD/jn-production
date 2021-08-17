from datetime import timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}
with DAG(
    'sgd',
    default_args={'owner': 'airflow'},
    description='A model sgd DAG',
    start_date=days_ago(1),
    schedule_interval=None,
    tags=['sgd'],
) as dag:
    t1 = BashOperator(
        task_id='launch_sgd',
        bash_command='python predict/src/api/sgd.py',
    )

    t1
