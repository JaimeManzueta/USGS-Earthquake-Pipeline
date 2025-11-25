import requests
import os 
import json




def get_data(url):
    

    response = requests.request("GET", url)

    print(response)
    
  

def main():

    get_data("https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=2025-11-01&endtime=2025-11-14&minmagnitude=4.5&orderby=time")






if __name__ == "__main__":
    main()