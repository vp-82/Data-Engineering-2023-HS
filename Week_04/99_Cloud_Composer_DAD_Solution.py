from airflow import DAG
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from airflow.providers.google.cloud.operators.bigquery import (
    BigQueryCreateEmptyDatasetOperator,
    BigQueryCreateEmptyTableOperator,
    BigQueryDeleteTableOperator,
)
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from google.cloud import storage
import json

# Define your DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'retries': 1,
}
dag = DAG(
    'load_csv_to_bigquery',
    default_args=default_args,
    description='Load CSV data from GCS to BigQuery',
    schedule_interval='@once',
)

# Define your variables
dataset_name = 'crime_dataset'
table_name = 'crime_data'
gcs_bucket = 'your_gcs_bucket_name'
gcs_schema_object = 'path_to_your_schema/crime_data_schema.json'

def get_schema_from_gcs(bucket_name, schema_file_path, **kwargs):
    # Initialize a GCS client
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    # Get the schema file from GCS
    blob = bucket.blob(schema_file_path)
    schema_json = blob.download_as_text()

    # Push the schema to XCom
    kwargs['task_instance'].xcom_push(key='schema', value=json.loads(schema_json))

# Use PythonOperator in your DAG
get_schema = PythonOperator(
    task_id='get_schema',
    python_callable=get_schema_from_gcs,
    op_args=['your_gcs_bucket_name', 'path_to_schema_file_in_gcs'],
    provide_context=True,
    dag=dag,
)

# Step 1: Check/Create Dataset
create_dataset = BigQueryCreateEmptyDatasetOperator(
    task_id='create_dataset',
    dataset_id=dataset_name,
    dag=dag,
)

# Step 2: Delete Table (if exists)
delete_table = BigQueryDeleteTableOperator(
    task_id='delete_table',
    deletion_dataset_table=f"{dataset_name}.{table_name}",
    ignore_if_missing=True,
    dag=dag,
)

# Step 3: Check/Create Table
create_table = BigQueryCreateEmptyTableOperator(
    task_id='create_table',
    dataset_id=dataset_name,
    table_id=table_name,
    schema_fields="{{ task_instance.xcom_pull(task_ids='load_schema_to_xcom', key='return_value') }}",
    dag=dag,
)

# Step 4: Load Data
load_csv = GCSToBigQueryOperator(
    task_id='load_csv',
    bucket=gcs_bucket,
    source_objects=['crime_data/crime_robbery.csv', 'crime_data/crime_burglary.csv'],
    destination_project_dataset_table=f"{dataset_name}.{table_name}",
    skip_leading_rows=1,
    write_disposition='WRITE_APPEND',
    field_delimiter=';',
    schema_fields="{{ task_instance.xcom_pull(task_ids='load_schema_to_xcom', key='return_value') }}",
    dag=dag,
)

# Define the task dependencies
create_dataset >> get_schema >> delete_table >> create_table >> load_csv

