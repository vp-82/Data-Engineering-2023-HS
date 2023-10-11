# Data Engineering Exercise: Building an ETL Pipeline with Apache Airflow

## Objective

Develop a scalable and automated data pipeline using Apache Airflow to manage the ETL process of loading data from Google Cloud Storage (GCS) to BigQuery.

## Setup Guidelines

Refer to the setup guide provided in `01_Cloud_Composer_Exercise_Setup.md` for instructions on setting up your GCP environment.

## DAG Skeleton

Below is the DAG skeleton that you will complete as part of this exercise.

```python
# Importing necessary libraries
from airflow import DAG
from airflow.providers.google.cloud.operators.bigquery import (
    BigQueryCreateEmptyDatasetOperator,
    BigQueryDeleteTableOperator,
    BigQueryCreateEmptyTableOperator,
)
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from airflow.providers.google.cloud.transfers.gcs_to_variable import GoogleCloudStorageToVariableOperator
from airflow.utils.dates import days_ago

# Your code starts here

# Task 1: Define the Variables
# HINT: Define your variables (dataset_name, table_name, gcs_bucket, gcs_schema_object) using the given hints in the task description.

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
    # HINT: Define the dataset_id parameter using the previously defined variable.
    # Your code ends here
    dag=dag,
)

# Task 3: Load Schema
load_schema = GoogleCloudStorageToVariableOperator(
    task_id='load_schema',
    # Your code starts here
    # HINT: Define bucket and object_name parameters using the previously defined variables.
    # Your code ends here
    variable_name='schema',
    dag=dag,
)

# Task 4: Delete Table (if exists)
delete_table = BigQueryDeleteTableOperator(
    task_id='delete_table',
    # Your code starts here
    # HINT: Define the deletion_dataset_table parameter using the previously defined variables.
    # Your code ends here
    ignore_if_missing=True,
    dag=dag,
)

# Task 5: Check/Create Table
create_table = BigQueryCreateEmptyTableOperator(
    task_id='create_table',
    # Your code starts here
    # HINT: Define dataset_id, table_id, and schema_fields parameters using the previously defined variables.
    # Your code ends here
    dag=dag,
)

# Task 6: Load Data to BigQuery
load_data = GCSToBigQueryOperator(
    task_id='load_data',
    # Your code starts here
    # HINT: Define bucket, source_objects, destination_project_dataset_table, schema_fields, and other parameters as needed.
    # Your code ends here
    dag=dag,
)

# Task 7: Set Task Dependencies
# Your code starts here
# HINT: Ensure tasks run in the correct order by setting their dependencies using >> and << operators.
# Your code ends here
```

### Task 1: Define the Variables

#### Hints (1)

Define variables that will be used to specify dataset names, table names, GCS bucket names, and GCS schema object paths.

```python
dataset_name = 'your_dataset_name'
table_name = 'your_table_name'
gcs_bucket = 'your_gcs_bucket_name'
gcs_schema_object = 'path_to_your_schema.json'
```

### Task 2: Check/Create Dataset

#### Hints (2)

Use `BigQueryCreateEmptyDatasetOperator` to check for or create the dataset in BigQuery.

```python
create_dataset = BigQueryCreateEmptyDatasetOperator(
    task_id='create_dataset',
    dataset_id=dataset_name,  # use the variable defined in Task 1
    dag=dag,
)
```

### Task 3: Load Schema

#### Hints (3)

Use `GoogleCloudStorageToVariableOperator` to load the schema from GCS and store it in an XCom variable.

```python
load_schema = GoogleCloudStorageToVariableOperator(
    task_id='load_schema',
    bucket=gcs_bucket,  # use the variable defined in Task 1
    object_name=gcs_schema_object,  # use the variable defined in Task 1
    variable_name='schema',
    dag=dag,
)
```

### Task 4: Delete Table (if exists)

#### Hints (4)

Use `BigQueryDeleteTableOperator` to delete the table in BigQuery if it exists.

```python
delete_table = BigQueryDeleteTableOperator(
    task_id='delete_table',
    deletion_dataset_table=f"{dataset_name}.{table_name}",  # use variables defined in Task 1
    ignore_if_missing=True,  # do not raise an error if the table does not exist
    dag=dag,
)
```

### Task 5: Check/Create Table

#### Hints (5)

Use `BigQueryCreateEmptyTableOperator` to create a new table in BigQuery.

```python
create_table = BigQueryCreateEmptyTableOperator(
    task_id='create_table',
    dataset_id=dataset_name,  # use the variable defined in Task 1
    table_id=table_name,  # use the variable defined in Task 1
    schema_fields="{{ task_instance.xcom_pull(task_ids='load_schema', key='return_value') }}",  # use XCom templating to retrieve the schema stored in Task 3
    dag=dag,
)
```

### Task 6: Load Data to BigQuery

#### Hints (6)

Use `GCSToBigQueryOperator` to load data from GCS to BigQuery.

```python
load_data = GCSToBigQueryOperator(
    task_id='load_data',
    bucket=gcs_bucket,  # use the variable defined in Task 1
    source_objects=['data_file1.csv', 'data_file2.csv'],  # specify your source data files
    destination_project_dataset_table=f"{dataset_name}.{table_name}",  # use variables defined in Task 1
    skip_leading_rows=1,  # adjust as per your data
    write_disposition='WRITE_APPEND',  # adjust as needed
    schema_fields="{{ task_instance.xcom_pull(task_ids='load_schema', key='return_value') }}",  # use XCom templating to retrieve the schema stored in Task 3
    dag=dag,
)
```

### Task 7: Set Task Dependencies

#### Hints (7)

Use the bitshift operators (>>, <<) or `set_downstream` and `set_upstream` methods to set the task dependencies.

```python
# Using bitshift operators
create_dataset >> load_schema >> delete_table >> create_table >> load_data

# OR using set_downstream and set_upstream methods
create_dataset.set_downstream(load_schema)
load_schema.set_downstream(delete_table)
delete_table.set_downstream(create_table)
create_table.set_downstream(load_data)
```
