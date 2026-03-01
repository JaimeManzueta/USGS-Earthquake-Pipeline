
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
def transform_data(data):
    # If the metadata status is there (200) then give me the data
    if data.get("metadata", {}).get("status") == 200:
        # initialize in A list first 
        data_stored = []
        # accessing the data's dictionary on the api web - {only access to the first data} - Used some AI for help on this 
        for feature in data.get("features", []):
            properties = feature.get("properties", {})        

        # gathering only the important and relevent data from the dictionary
            magnitude = properties.get("mag")
            place = properties.get("place")
            nst = properties.get("nst")
            felt = properties.get("felt")
            significance = properties.get("sig") 

        # store it into the data_stored
            current_record = {
                "magnitude: ": magnitude,
                "Place: ": place,
                "nst: ": nst,
                "felt: ": felt,
                "Significance: ": significance

            }
            
            data_stored.append(current_record)


        return data_stored



# Processing the Sql in order to automate it into the DB---------------------
# Loading the Clean Data into Postgres DB-------------------------------------------
@task
def load_data(transformed_data):
    earthq_database_hook = PostgresHook()
    earthq_database_conn = earthq_database_hook.get


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
    



# Combining everything together------------------------------------------
extract = extract_data()
transformed = transform_data(extract)
load_data(transformed)


