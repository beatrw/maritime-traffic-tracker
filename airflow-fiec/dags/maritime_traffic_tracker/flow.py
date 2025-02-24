from airflow import DAG
from datetime import datetime, timedelta
from airflow.models.xcom_arg import XComArg
from airflow.operators.python import PythonOperator
from airflow.models import TaskInstance
from airflow.operators.dummy import DummyOperator

from maritime_traffic_tracker.tasks.get_params import CalculateParams
from maritime_traffic_tracker.tasks.landing_task import DataExtractor
from maritime_traffic_tracker.tasks.transform_task import DataTrasformer
from maritime_traffic_tracker.tasks.business_atracacao_task import AtracacaoRulesInjector
from maritime_traffic_tracker.tasks.business_carga_task import CargaRulesInjector

default_args = {
    'start_date':datetime(2025, 2, 24),
    # 'email':['beatrizaquino_o@hotmail.com'],
    # 'email_on_failure':True,
    # 'email_on_retry':True,
    'retries':3,
    'retry_delay':timedelta(minutes=1)}


with DAG(
    dag_id='maritime_traffic_tracker_pipeline',
    default_args=default_args,
    start_date=datetime(2024, 9, 14),
    description='ETL de dados de tráfego marítimo',
    tags=['tracker'],
    schedule_interval= '0 0 1 * * ', #Dia 1 de cada mês
    catchup=False
) as dag:

    start = DummyOperator(task_id='start')

    get_params = PythonOperator(
        task_id='get_params',
        python_callable=CalculateParams().execute,
        do_xcom_push=True,
        )

    landing_task = PythonOperator.partial(
            task_id=f'landing_task',
            python_callable=DataExtractor().execute,
            max_active_tis_per_dag=1,
    ).expand(
        op_args=XComArg(get_params)
    )

    transform_task = PythonOperator(
        task_id='transform_task',
        python_callable=DataTrasformer().execute)

    business_atracacao_task = PythonOperator(
        task_id='business_atracacao_task',
        python_callable=AtracacaoRulesInjector().execute)

    business_carga_task = PythonOperator(
        task_id='business_carga_task',
        python_callable=CargaRulesInjector().execute)

    end = DummyOperator(task_id='end')

start >> \
    get_params >> \
    landing_task >> \
    transform_task >> \
    business_atracacao_task >> \
    business_carga_task >> \
end
