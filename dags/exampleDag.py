from airflow import DAG
from airflow.operators import BashOperator
from datetime import datetime, timedelta
"""
Example dags for play around.
"""

# Following are defaults which can be overridden later on
default_args = {
    'owner': 'awanish',
    'depends_on_past': False,
    'start_date': datetime.now(),
    'email': ['awanish00@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

dag = DAG('Helloworld', default_args=default_args, start_date=datetime(2020, 11, 12),
          schedule_interval=timedelta(minutes=1))

# t1, t2, t3 and t4 are examples of tasks created using operators

t1 = BashOperator(
    task_id='task_1',
    bash_command='echo "Hello World from Task 1"',
    dag=dag)

t2 = BashOperator(
    task_id='task_2',
    bash_command='echo "Hello World from Task 2"',
    dag=dag)

t3 = BashOperator(
    task_id='task_3',
    bash_command='echo "Hello World from Task 3"',
    dag=dag)

t4 = BashOperator(
    task_id='task_4',
    bash_command='echo "Hello World from Task 4"',
    dag=dag)

t2.set_upstream(t1)
t3.set_upstream(t1)
t4.set_upstream(t2)
t4.set_upstream(t3)