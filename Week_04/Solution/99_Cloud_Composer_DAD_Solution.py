from airflow import DAG
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateEmptyDatasetOperator
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
project_id = 'zhaw-data-engineering-2023'
dataset_name = 'crime_dataset'
table_name = 'crime_data'
gcs_bucket = 'zhaw-de-2023-pect-data-bucket'
gcs_schema_object = 'schema.json'
schema_fileds = [
    {"name": "INCIDENT_NUMBER", "type": "STRING", "mode": "NULLABLE"},
    {"name": "OFFENSE_CODE", "type": "INTEGER", "mode": "NULLABLE"},
    {"name": "OFFENSE_CODE_GROUP", "type": "STRING", "mode": "NULLABLE"},
    {"name": "OFFENSE_CODE_GROUP_No", "type": "INTEGER", "mode": "NULLABLE"},
    {"name": "OFFENSE_DESCRIPTION", "type": "STRING", "mode": "NULLABLE"},
    {"name": "DISTRICT", "type": "STRING", "mode": "NULLABLE"},
    {"name": "District_simple", "type": "STRING", "mode": "NULLABLE"},
    {"name": "District_simple_No", "type": "INTEGER", "mode": "NULLABLE"},
    {"name": "REPORTING_AREA", "type": "INTEGER", "mode": "NULLABLE"},
    {"name": "OCCURRED_ON_DATE", "type": "STRING", "mode": "NULLABLE"},
    {"name": "Hour1", "type": "STRING", "mode": "NULLABLE"},
    {"name": "Start_Night", "type": "STRING", "mode": "NULLABLE"},
    {"name": "Start_Day", "type": "STRING", "mode": "NULLABLE"},
    {"name": "Night_Day", "type": "STRING", "mode": "NULLABLE"},
    {"name": "YEAR", "type": "INTEGER", "mode": "NULLABLE"},
    {"name": "MONTH", "type": "INTEGER", "mode": "NULLABLE"},
    {"name": "DAY_OF_WEEK", "type": "STRING", "mode": "NULLABLE"},
    {"name": "WE_Workday", "type": "STRING", "mode": "NULLABLE"},
    {"name": "WE_Workday_No", "type": "INTEGER", "mode": "NULLABLE"},
    {"name": "HOUR", "type": "INTEGER", "mode": "NULLABLE"},
    {"name": "Counts_per_hour", "type": "INTEGER", "mode": "NULLABLE"},
    {"name": "STREET", "type": "STRING", "mode": "NULLABLE"},
    {"name": "Lat", "type": "FLOAT", "mode": "NULLABLE"},
    {"name": "Long", "type": "FLOAT", "mode": "NULLABLE"},
    {"name": "Location", "type": "STRING", "mode": "NULLABLE"}
]

# Check/Create Dataset
create_dataset = BigQueryCreateEmptyDatasetOperator(
    task_id='create_dataset',
    dataset_id=dataset_name,
    project_id=project_id,
    exists_ok=True,
    dag=dag,
)

# Load Data
load_csv = GCSToBigQueryOperator(
    task_id='load_csv',
    bucket=gcs_bucket,
    source_objects=['crime_robbery.csv', 'crime_burglary.csv'],
    destination_project_dataset_table=f"{dataset_name}.{table_name}",
    skip_leading_rows=1,
    write_disposition='WRITE_TRUNCATE',
    field_delimiter=';',
    schema_fields=schema_fileds,
    dag=dag,
)

# Define the task dependencies
create_dataset >> load_csv
