# All of the Libraries-----------------------------------
import requests
import os 
import json
import pandas as pd 

# Extracted Raw Data----------------------------------------------------

# Access the data using request to access the html of the api website 
def get_data(url):
    response = requests.get(url)
    # Convert it into .json 
    get_data = response.json()

    return get_data

# Transforming Raw Data Into Clean Data----------------------------------------
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


        # store it into the data_stored
            current_record = {
                "magnitude: ": magnitude,
                "Place: ": place,
                "nst: ": nst,
                "felt: ": felt
            }
            
            data_stored.append(current_record)


        return data_stored

    
# Loading the Clean Data into the DB (postgres)---------------------------------------

def Loading():
    pass










  
# Gathering everything inside this main--------------------------------------------- 
def main():
    api = "https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=2025-11-01&endtime=2025-11-14&minmagnitude=4.5&orderby=time"
    fetched_data = get_data(api)
    trans_data = transform_data(fetched_data)

    print(trans_data)



if __name__ == "__main__":
    main()