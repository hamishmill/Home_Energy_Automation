import requests


def get_battery_SOC():




    #enter url 
    service_url = "ENTER URL HERE"

    #enter token
    token = "ENTER TOKEN HERE"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }


# parameters to go with the action
    data = {} 
        

# Send the POST request to turn on the light
    response = requests.get(service_url, headers=headers, json=data)

# Check the response
    if response.status_code == 200:
        data = response.json()
        state = data['state']
        return state  
        
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return f"Error: {response.status_code} - {response.text}"