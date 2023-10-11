# Data Engineering Exercise: Building an ETL Pipeline with Apache Airflow

## Objective

Develop a scalable and automated data pipeline using Apache Airflow to manage the ETL process of loading data from Google Cloud Storage (GCS) to BigQuery.

## Setup Guidelines

### Prerequisites

- Ensure you have access to Google Cloud Platform with billing set up.
- Ensure `gcloud` and `bq` CLI tools are installed and authenticated.

### Predefined Values

- **GCP Project ID**: `zhaw-data-engineering-2023`
- **Service Account Name**: `de-2023-service-account`
- **Display Name**: `Data Engineering 2023 Service Account`
- **Key Path**: `de-2023-service-account-key.json`
- **Cloud Composer Environment Name**: `de-2023-airflow-env`
- **Location for Cloud Composer**: `europe-west6` (Switzerland nearby region)
- **Zone for Cloud Composer**: `europe-west6-a`
- **Disk Size for Cloud Composer**: `20GB`
- **Machine Type for Cloud Composer**: `composer-n1-standard-2`

### Commands

```bash
# Create a new GCP project
# Make sure to replace [BILLING_ACCOUNT_ID] with your billing account ID
gcloud projects create zhaw-data-engineering-2023 --name="ZHAW Data Engineering 2023"
gcloud beta billing projects link zhaw-data-engineering-2023 --billing-account=[BILLING_ACCOUNT_ID]

# Set the GCP project
gcloud config set project zhaw-data-engineering-2023

# Enable necessary APIs
gcloud services enable bigquery.googleapis.com
gcloud services enable storage-api.googleapis.com
gcloud services enable composer.googleapis.com

# Create a service account
gcloud iam service-accounts create de-2023-service-account --display-name "Data Engineering 2023 Service Account"

# Create and download a JSON key for the service account
gcloud iam service-accounts keys create de-2023-service-account-key.json --iam-account de-2023-service-account@zhaw-data-engineering-2023.iam.gserviceaccount.com

# Assign roles to the service account
gcloud projects add-iam-policy-binding zhaw-data-engineering-2023 --member="serviceAccount:de-2023-service-account@zhaw-data-engineering-2023.iam.gserviceaccount.com" --role="roles/bigquery.user"
gcloud projects add-iam-policy-binding zhaw-data-engineering-2023 --member="serviceAccount:de-2023-service-account@zhaw-data-engineering-2023.iam.gserviceaccount.com" --role="roles/bigquery.dataEditor"
gcloud projects add-iam-policy-binding zhaw-data-engineering-2023 --member="serviceAccount:de-2023-service-account@zhaw-data-engineering-2023.iam.gserviceaccount.com" --role="roles/storage.objectAdmin"

# Create a Cloud Composer environment (optional)
gcloud composer environments create de-2023-airflow-env --location=europe-west6 --zone=europe-west6-a --disk-size=20GB --machine-type=composer-n1-standard-2

# Create a GCS bucket
# Make sure to replace [SHORTNAME] with your unique short name
gsutil mb -p zhaw-data-engineering-2023 -l europe-west6 gs://zhaw-de-2023-[SHORTNAME]-data-bucket/

# Upload data files to the GCS bucket
# Make sure to replace [PATH_TO_LOCAL_FILE] with the local path to your file
gsutil cp [PATH_TO_LOCAL_FILE]/crime_robbery.csv gs://zhaw-de-2023-[SHORTNAME]-data-bucket/
gsutil cp [PATH_TO_LOCAL_FILE]/crime_burglary.csv gs://zhaw-de-2023-[SHORTNAME]-data-bucket/

# (Optional) Upload schema file to the GCS bucket
# Make sure to replace [PATH_TO_LOCAL_FILE] with the local path to your file
gsutil cp [PATH_TO_LOCAL_FILE]/schema.json gs://zhaw-de-2023-[SHORTNAME]-data-bucket/
```
