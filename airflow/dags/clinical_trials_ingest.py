from __future__ import annotations

from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator


def ingest_task(**context):
    # Placeholder ingest; integrate with app.rag.ingest
    print("Ingest job placeholder: refresh FAISS index")


with DAG(
    dag_id="clinical_trials_ingest",
    schedule_interval="@daily",
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["ctc"],
) as dag:
    run = PythonOperator(task_id="run_ingest", python_callable=ingest_task)

