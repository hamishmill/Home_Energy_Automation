import requests
from datetime import date, timedelta
import pandas as pd

def get_solcast_forecast():
# Enter panel IDs
    solar_strings = ["ENTER PANEL HERE", "IF MULTIPLE ENTER ANOTHER HERE"]  # SE, SW
    headers = {'Authorization': 'ENTER KEY HERE'}

    # store all the predictions
    all_predictions = []

    # Fetch predictions for each panel
    for rooftop_resource_id in solar_strings:
        url = f"https://api.solcast.com.au/rooftop_sites/{rooftop_resource_id}/forecasts?format=json"
    #api request to return the info
        response = requests.get(url, headers=headers)
    
        if response.status_code == 200:
        # parse the json data and get the forecast part of it
            forecast_data = response.json().get('forecasts')
            all_predictions.extend(forecast_data)
        else:
            print(f"Error: Got status code {response.status_code} for {rooftop_resource_id}")

    all_predictions
    #Turn JSON data into a dataframe
    prediction_dataframe = pd.DataFrame(all_predictions)

    #First turn the datatypes to datetime as before they are string???? Stores the casted data in a new column
    prediction_dataframe['date'] = pd.to_datetime(prediction_dataframe['period_end'])
    #  this truncates the time part
    prediction_dataframe['date'] = prediction_dataframe['date'].dt.date

    #print(prediction_dataframe)
    tomorrow = date.today() + timedelta(days = 1)
    #sum all the values that match up with tomorrows date specifically
    tomorrow_predicted_pv = prediction_dataframe[prediction_dataframe['date'] == tomorrow]['pv_estimate'].sum()/2
    print(tomorrow_predicted_pv)
    return tomorrow_predicted_pv
