import os 
import requests 
from datetime import datetime
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
def earthquake_pipeline():

    
    # My first task that will extract the Data-------------------------------
    @task
    def extract_data(data_interval_start, data_interval_end, **kargs ):

        # This will be the time converted into ISO 8601 Format: "2026-10-28T10:09:30"
        time_start_str = data_interval_start.isoformat()
        time_end_str = data_interval_end.isoformat()


        # this is the parameter of the url link: we are turning this autonomous 
        params = {
            "starttime": time_start_str,
            "endtime"  : time_end_str,
            "format"   : "geojson",
            "eventtype"    : "earthquake",
            "minmagnitude": 4.5,
            "orderby"  : "time-asc",
        
        }

        # API URL Link 
        url = "https://earthquake.usgs.gov/fdsnws/event/1/query"
       
        # implementing both url and parameters, it times out in 30 secs if it didnt work 
        response = requests.get(url, params=params, timeout=30)

        # it will give me 200 if the server has reached back or 400 for an error 
        response.raise_for_status()

        status_code1 = response.status_code


        # if the status code receives 204 it means that their isnt any data to extract today 
        if status_code1 == 204:
           print("No Earthquake Data Today")
           met_data = {
               # the resposen was successful 
                "metadata": {"status": 200},
               # however transform check for this and it will be empty
                "features": []
            }
           # then it goes to the next function 
           return met_data
        
        else:
            # if i do have data available it will return in a json form and move on to the next function 
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
                    "magnitude": magnitude,
                    "place": place,
                    "nst": nst,
                    "felt": felt,
                    "significance": significance
    }
                
                data_stored.append(current_record)


            return data_stored



    # Processing the Sql in order to automate it into the DB---------------------
    # Loading the Clean Data into Postgres DB-------------------------------------------
    @task
    def load_data(transformed_data):
        earthq_database_hook = PostgresHook(postgres_conn_id="quake_pg_conn")
        conn = earthq_database_hook.get_conn()
        cursor = conn.cursor()

        # Create the table if it doanst exist

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS quakes(
                place VARCHAR(255),
                magnitude NUMERIC,
                felt INT,
                significance INT,
                nst INT
            );
        """)
        # Inserting on each record 
        for record in transformed_data:
            cursor.execute("""
                INSERT INTO quakes (place, magnitude, felt, significance, nst)
                VALUES (%s, %s, %s, %s, %s)""",
                (
                record["place"],
                record["magnitude"],
                record["felt"],
                record["significance"],
                record["nst"]
            ))
        # closing once its done 
        conn.commit()
        cursor.close()
        conn.close()



    # Combining everything together------------------------------------------
    extract = extract_data()
    transformed = transform_data(extract)
    load_data(transformed)

# Instantiate the DAG
earthquake_pipeline() 