# Importing necessary libraries
from airflow import DAG
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateEmptyDatasetOperator
from airflow.utils.dates import days_ago


# Task 1
# Define your variables (project_id, dataset_name, table_name, gcs_bucket)
# Your code starts here

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

# Task 2: Check/Create Dataset
create_dataset = BigQueryCreateEmptyDatasetOperator(
    task_id='create_dataset',
    # Your code starts here
    # Define dataset_id and project_id parameters
    # Your code ends here
    dag=dag,
)

# Task 3: Load Data
load_csv = GCSToBigQueryOperator(
    task_id='load_csv',
    # Your code starts here
    # Define bucket, source_objects, destination_project_dataset_table,
    # skip_leading_rows, write_disposition, field_delimiter, 
    # and schema_fields parameters
    # Your code ends here
    dag=dag,
)

# Task 4: Define the task dependencies
# Your code starts here
# Set the order of tasks
# Your code ends here
