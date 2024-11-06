from functions.get_solcast_forecast import get_solcast_forecast
from functions.get_weekly_average import get_weekly_average
from functions.set_battery import set_battery_charge

def configure_battery():
    #get consumption
    daily_totals = get_weekly_average()
    average_consumption = sum(daily_totals)/len(daily_totals)

    #get forecast
    #tomorrow_forecast = get_solcast_forecast()
    tomorrow_forecast = 16
    print(tomorrow_forecast, average_consumption)
    
    if tomorrow_forecast > average_consumption:
        #makes the api call
        set_battery_charge(4)

    else:
        #makes the api call
        set_battery_charge(50)   

    return  
configure_battery()
 