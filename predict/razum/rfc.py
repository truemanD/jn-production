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
    'rfc',
    default_args={'owner': 'airflow'},
    description='A model rfc DAG',
    start_date=days_ago(1),
    schedule_interval=None,
    tags=['rfc'],
) as dag:
    t1 = BashOperator(
        task_id='launch_rfc',
        bash_command='python predict/src/api/rfc.py',
    )

    t1
