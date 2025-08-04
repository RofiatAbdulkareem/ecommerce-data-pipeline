from datetime import datetime

from airflow.operators.python import PythonOperator

from airflow import DAG
from airflow.dags.api_to_rds import (fetch_data_from_api, read_from_s3,
                                     upload_to_rds, upload_to_s3)

default_args = {
    'owner': 'rofiat',
    'retries': 1,
    'start_date': datetime(2025, 7, 30),
}

dag = DAG(
    dag_id="ecommerce_data_pipeline",
    description="Extracts and loads products\
        data to postgres RDS daily at 10am",
    default_args=default_args,
    schedule_interval="0 10 * * *",
    catchup=False,
)

extract_data = PythonOperator(
    task_id="extract_products_data",
    python_callable=fetch_data_from_api,
    dag=dag
)

write_to_s3 = PythonOperator(
    task_id="load_products_data_to_s3",
    python_callable=upload_to_s3,
    dag=dag
)

extract_from_s3 = PythonOperator(
    task_id="extract_products_data_from_s3",
    python_callable=read_from_s3,
    dag=dag
)

write_to_rds = PythonOperator(
    task_id="load_products_data_to_RDS",
    python_callable=upload_to_rds,
    dag=dag
)
extract_data >> write_to_s3 >> extract_from_s3 >> write_to_rds
