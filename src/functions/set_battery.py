import requests

def set_battery_charge(value):

# Home Assistant API URL for setting the battery charge value

    #enter url 
    light_service_url = "ENTER URL HERE"

    #enter token
    token = "ENTER TOKEN HERE"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

# parameters to go with the action
    data = {
        "entity_id": "number.givtcp_sa2243g060_target_soc" , 
        "value" : value
    }

# Send the POST request to turn on the light
    response = requests.post(light_service_url, headers=headers, json=data)

# Check the response
    if response.status_code == 200:
        print("charge target set")
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return