import os 
import requests 
import datetime 
import pendulum

from airflow.sdk import task, dag
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator


@dag("Earthquake_dag",
     start_date = pendulum.datetime(2021,1,1),
     schedule = "0 0 * * *",
     catchup = False,
     dagrun_timeout = datetime.timedelta(minutes = 60),

)

def processing_quakes():
    create_quakes_table = SQLExecuteQueryOperator(
        task_id = "create_quake_table",
        conn_id = "quake_pg_conn",
        sql = """
          CREATE TABLE IF NOT EXIST quakes(
          "id" NUMERIC PRIMARY KEY,
          "place" VARCHAR(255),
          "magnitude" INT,
          "felt" INT,
          "status" VARCHAR(255),
          "rms" INT,
          "dmin" INT,
          "nst" INT,
          "cdi" INT
          ); """,    
    )


@task


@task
def getting_data():
    pass
