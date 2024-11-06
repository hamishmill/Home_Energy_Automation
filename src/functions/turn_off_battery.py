import requests

def turn_battery_off():




    #enter url 
    service_url = f"ENTER URL HERE"

    #enter token
    token = "ENTER TOKEN HERE"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

# parameters to go with the action
    data = {
        "entity_id": "switch.givtcp_sa2243g060_enable_discharge" , 
    }

# Send the POST request to turn on the light
    response = requests.post(service_url, headers=headers, json=data)

# Check the response
    if response.status_code == 200:
        print(f'success battery has been turned off')
        # Filter or print the services related to a specific domain if needed
        

    else:
        print(f"Error: {response.status_code} - {response.text}")
        return
