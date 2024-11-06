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

    #initialise as 0
    num_days = 0 
    #which previous date we want to look at
    day = today - timedelta(days = num_days)
    
    #initialise array to store cumulative results
    weekly_interval_array = [0] * 48

    for i in range(0,7):


        #set initial date starting yesterday
        num_days += 1
        day = today - timedelta(days = num_days)
        #creates the json data response
        historic_givenergy_data = fetch_data_points(API_KEY, inverter_serial_number, day)
        #turns the json data into a pandas df
        daily_total = pd.json_normalize(historic_givenergy_data)

        #subset of full df

    #turn time column from string into time
        daily_total['time'] = pd.to_datetime(daily_total['time'])
    #sorts them into halfhour sections

        daily_total['HalfHourInterval'] = daily_total['time'].dt.floor('30T')

        interval_consumption = daily_total.groupby('HalfHourInterval').last().reset_index()
        cumulative_consumption_array = interval_consumption['today.consumption'].tolist()

    #initialise array to store results
        interval_consumption_array = [0] * 48
        
        #copy over first values
        interval_consumption_array[0] = cumulative_consumption_array[0]
        weekly_interval_array[0] += interval_consumption_array[0]
        for i in range(1,len(cumulative_consumption_array)):

            interval_consumption_array[i] = cumulative_consumption_array[i] - cumulative_consumption_array[(i-1)]
            weekly_interval_array[i] += interval_consumption_array[i]
        
    weekly_interval_array = np.array(weekly_interval_array) /7 
       
        

    return weekly_interval_array