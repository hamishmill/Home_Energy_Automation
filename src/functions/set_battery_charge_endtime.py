import requests
from datetime import datetime, timedelta

def set_charge_end():




    #enter url 
    service_url = f"ENTER URL HERE"

    #enter token
    token = "ENTER TOKEN HERE"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    #select the next minute to quickly start charge
    now = datetime.now()
    end_minute = (now + timedelta(minutes=30)).replace(second=0, microsecond=0)
    end_time = end_minute.strftime("%H:%M:%S")



# parameters to go with the action
    data = {
        "entity_id": "select.givtcp_sa2243g060_charge_end_time_slot_1" , 
        "option": f"{end_time}"
    }




# Send the POST request to turn on the light
    response = requests.post(service_url, headers=headers, json=data)

# Check the response
    if response.status_code == 200:
        print('success')
        

    else:
        print(f"Error: {response.status_code} - {response.text}")
        return