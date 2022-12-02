"""Backend to contact the IDFM api."""


import requests
import json


BASE_URL ="https://api-iv.iledefrance-mobilites.fr/lines/v2/"

# line:IDFM:C01561
# # stop_area:IDFM:420704
def request_data(line, stop_area):
    endpoint = f"{BASE_URL}/line:IDFM:{line}/stops/stop_area:IDFM:{stop_area}/realTime"

    response = requests.get(endpoint).json()

    data = response['nextDepartures']['data']
    statusCode = response['nextDepartures']['statusCode']
    errorMessage = response['nextDepartures']['errorMessage']


    return data, statusCode, errorMessage
