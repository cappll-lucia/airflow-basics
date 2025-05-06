from airflow import DAG, Dataset
from airflow.decorators import task

from datetime import datetime

file = Dataset("/tmp/file.txt")
file2 = Dataset("/tmp/file2.txt")

with DAG(
    dag_id="producer",
    schedule="@daily",
    start_date=datetime(2025,1,1,),
    catchup=False
):
    
    @task(outlets=[file])
    def update_dataset():
        with open(file.uri, "a+") as f:
            f.write("producer updated")

    @task(outlets=[file2])
    def update_dataset2():
        with open(file2.uri, "a+") as f:
            f.write("producer updated")
    
    update_dataset() >> update_dataset2()