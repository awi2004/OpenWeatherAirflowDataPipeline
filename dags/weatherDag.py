import pickle
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators import PythonOperator
import os
from airflow.hooks import PostgresHook
import json
import numpy as np

# list of cities which is used to get weather details.
cities = ['Patna', 'Dresden', 'Berlin', 'Cologne', 'Delhi', 'Mumbai']


def load_data(ds, **kwargs):
    """
	Processes the json data, checks the types and enters into the
	Postgres database.

	"""

    pg_hook = PostgresHook(postgres_conn_id='weather_id')

    # file_name = str(datetime.now().date()) + '_Dresden' + '.json'
    # tot_name = os.path.join(os.path.dirname(__file__), 'src/data', file_name)
    pickle_dir_name = os.path.join(os.path.dirname(__file__), 'src/data', 'weather.obj')
    doc = pickle.load(open(pickle_dir_name, 'rb'))
    # open the json datafile and read it in
    # with open(tot_name, 'r') as inputfile:
    #    doc = json.load(inputfile)

    for i in range(0, len(doc)):

        # transform the data to the correct types and convert temp to celsius
        city = str(doc[i]['name'])
        country = str(doc[i]['sys']['country'])
        lat = float(doc[i]['coord']['lat'])
        lon = float(doc[i]['coord']['lon'])
        humid = float(doc[i]['main']['humidity'])
        press = float(doc[i]['main']['pressure'])
        min_temp = float(doc[i]['main']['temp_min']) - 273.15
        max_temp = float(doc[i]['main']['temp_max']) - 273.15
        temp = float(doc[i]['main']['temp']) - 273.15
        weather = str(doc[i]['weather'][0]['description'])
        todays_date = datetime.now().date()

        # check for nan's in the numeric values and then enter into the database
        valid_data = True
        for valid in np.isnan([lat, lon, humid, press, min_temp, max_temp, temp]):
            if valid is False:
                valid_data = False
                break;

        row = (city, country, lat, lon, todays_date, humid, press, min_temp,
               max_temp, temp, weather)

        insert_cmd = """INSERT INTO weather_table 
                        (city, country, latitude, longitude,
                        todays_date, humidity, pressure, 
                        min_temp, max_temp, temp, weather)
                        VALUES
                        (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""

        if valid_data is True:
            pg_hook.run(insert_cmd, parameters=row)


# Define the default dag arguments.
default_args = {
    'owner': 'awanish',
    'depends_on_past': False,
    'email': ['awanish00@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 3,
    'retry_delay': timedelta(minutes=1)
}

# Define the dag, the start date and how frequently it runs.
# I chose the dag to run 12 times a day by choosing to run it every hour.
dag = DAG(
    dag_id='weatherDag',
    default_args=default_args,
    start_date=datetime(2020, 11, 12),
    schedule_interval=timedelta(minutes=60))

# for i in range(0, 3):
#    paramter = {'CITY': cities[i]}

# First task is to query get the weather from openweathermap.org and dump it via Pickle.
task1 = BashOperator(
    task_id='get_weather',

    bash_command="python ~/dags/src/getWeather.py   Dresden, Berlin, Hamburg ",  # '{{params.CITY}}'
    # params={'CITY': ['Dresden', 'Berlin', 'Hamburg']},
    # bash_command='python C:/Users/49176/PycharmProjects/WeatherETL/dags/src/getWeather.py',
    dag=dag)

# Second task is to process the data and load into the database.
task2 = PythonOperator(
    task_id='transform_load',
    provide_context=True,
    python_callable=load_data,
    dag=dag)

# Set task1 "upstream" of task2, i.e. task1 must be completed
# before task2 can be started.
task1 >> task2
