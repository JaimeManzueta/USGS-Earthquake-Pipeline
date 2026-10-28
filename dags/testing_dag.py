import requests


# testing out extract data function:
url = "https://earthquake.usgs.gov/fdsnws/event/1/query"


       
response = requests.get(url, timeout=30)

        # it will give me 200 if the server has reached back or 400 for an error 
response.raise_for_status()

status_code1 = response.status_code

if status_code1 == 204:
    print("No Earthquake Data Today")
else:
    print("theirs data")