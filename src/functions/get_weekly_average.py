import requests
import json
from datetime import date, timedelta
import numpy as np
import pandas as pd

def get_weekly_average():
    # Enter API Key
    API_KEY = 'ENTER API KEY HERE'
# Set the inverter serial number and the date
    inverter_serial_number = 'ENTER INVERTER SERIAL NUMBER HERE'  # Replace with your inverter's serial number
    

    def fetch_data_points(api_key, inverter_serial, day):
        base_url = f'https://api.givenergy.cloud/v1/inverter/{inverter_serial}/data-points/{day}'
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
    
        page = 1
        all_data = []
        #while true to loop through all pages for the day.
        while True:
            params = {
                'page': page
            }
        
            response = requests.get(base_url, headers=headers, params=params)

            if response.status_code == 200:
                data = response.json()
                all_data.extend(data['data'])  # Add the new data to our list
                page += 1  # Move to the next page
                #print(page)
            if not data['data']:
                break
    
        return all_data

    today = date.today()

    num_days = 1 
    #which previous date we want to look at
    day = today - timedelta(days = num_days)

    daily_totals = [0] * 7

    for i in range(0,7):
        #set initial date
        day = today - timedelta(days = num_days)
        #creates the json data response
        historic_givenergy_data = fetch_data_points(API_KEY, inverter_serial_number, day)
        #turns the json data into a pandas df
        historic_givenergy_dataframe = pd.json_normalize(historic_givenergy_data)
        #selects the value for total energy consumption in the house for that day and stores in a list
        daily_totals[i] = historic_givenergy_dataframe['today.consumption'].iloc[-1]

        num_days += 1
        print(num_days)

    return daily_totals