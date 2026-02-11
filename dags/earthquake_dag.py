import os 
import requests 
import datetime 
import pendulum

# Airflow setup with dag, postgreshook, and sql setup----------------------------- 
from airflow.sdk import task, dag
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator

# Creating the DAG thats going to show up in the airflow server------------------

@dag("Earthquake_dag",
     start_date = pendulum.datetime(2021,1,1),
     schedule = "0 0 * * *",
     catchup = False,
     dagrun_timeout = datetime.timedelta(minutes = 60),

)

# My first task that will extract the Data-------------------------------
@task
def extract_data():
    API = "https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=2025-11-01&endtime=2025-11-14&minmagnitude=4.5&orderby=time"
    response = requests.get(API)
    extracted = response.json()

    return extracted
    


# My Second Task that will Transform the raw Data into clean Data------------------
@task
# FIX: data_stored - it doasnt work with the function - cant implement it 
def transform_data():
    if data.get("metadata", {}).get("status") == 200:
        # turning the data into a list
        data_stored = []

        # Creating a Loop for the data:
        for feature in data.get("features", []):
            properties = feature.get("properties", {})


            
            magnitude = properties.get["mag"]
            place = properties.get["place"]
            nst = properties.get["nst"]
            felt = properties.get["felt"]


            # store it into the data_stored
            data_that_stored = {
                "magnitude: ": magnitude,
                "Place: ": place,
                "nst: ": nst,
                "felt: ": felt
            }
            data_stored.append(data_that_stored)


        return data_stored


# Processing the Sql in order to automate it into the DB---------------------

def sql_processing_quakes():
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

# Loading the Clean Data into DB-------------------------------------------
def load_data():
    pass
    




# Combining everything together------------------------------------------
