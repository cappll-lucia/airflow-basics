from airflow import DAG, Dataset
from airflow.decorators import task

from datetime import datetime

file = Dataset("/tmp/file.txt")
file2 = Dataset("/tmp/file2.txt")

with DAG(
    dag_id="consumer",
    schedule=[file, file2],
    start_date=datetime(2025,1,1,),
    catchup=False
):
    
    @task
    def read_dataset():
        with open(file.uri, "r") as f:
            print(f"--> {f.read}")
    
    read_dataset()
