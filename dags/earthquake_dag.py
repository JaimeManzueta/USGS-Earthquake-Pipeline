import os 
import requests 
import datetime 
import pendulum

from airflow.sdk import task, dag


@dag("Earthquake_dag",
     start_date = pendulum.datetime(2021,1,1),
     schedule = "0 0 * * *",
     catchup = False,
     dagrun_timeout = datetime.timedelta(minutes = 60),

)


@task





