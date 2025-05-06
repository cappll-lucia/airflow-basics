# basics-airflow

This repository contains example DAGs for learning Apache Airflow. It focuses on two core use cases:

1. A simple **ETL pipeline** using API + PostgreSQL
2. A **producer/consumer** pattern using the Dataset feature introduced in Airflow 2.4+

---

## 1. user_processing: API to PostgreSQL ETL Pipeline

This DAG performs an end-to-end data pipeline that:

1. Waits for an external API to become available (`HttpSensor`)
2. Fetches user data from the API (`SimpleHttpOperator`)
3. Processes the JSON into CSV format (`PythonOperator`)
4. Stores the processed data into a PostgreSQL table (`PostgresOperator` + `PostgresHook`)

### Tasks:
- `create_table`: Creates the `users` table if it doesn’t exist
- `is_api_available`: Polls the API until it’s ready
- `extract_user`: Sends a GET request to fetch user data
- `process_user`: Normalizes and writes the data to `/tmp/processed_user.csv`
- `store_user`: Copies the CSV into PostgreSQL using `COPY`

### Requirements:
- A connection named `postgres` in Airflow (PostgreSQL)
- A connection named `user_api` (HTTP API returning user JSON)

---

## 2. producer / consumer: Dataset-based Triggering

This example shows how to decouple DAGs using **Datasets**, which allow one DAG to trigger another based on file updates.

### `producer` DAG
- Runs daily and writes to two files:
  - `/tmp/file.txt`
  - `/tmp/file2.txt`
- Declares these files as `Dataset` outputs (`outlets`)
- Other DAGs can be triggered when these datasets are updated

### `consumer` DAG
- Has no regular schedule — it’s triggered **only** when `/tmp/file.txt` or `/tmp/file2.txt` changes
- Reads and prints the contents of these files

### Use Case:
This pattern is useful for separating **data production** and **data consumption**, keeping workflows modular and event-driven.

