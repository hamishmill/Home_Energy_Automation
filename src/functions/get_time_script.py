#Function for getting the timestep we are on
from datetime import datetime, timedelta

def get_time_state():



    #gets the current time as a datetime datatype
    now = datetime.now()
    #gets the minute we are on
    minutes = now.minute

    # round up to the nearest 30 if not already there
    if minutes % 30 != 0:
        next_interval = now + timedelta(minutes=(30 - minutes % 30))
    else:
        next_interval = now

    # remove seconds as we just care about 30 min intervals
    next_interval = next_interval.replace(second=0, microsecond=0)

    # calc what position in the arrays this would be at
    # start by retreiving the hours and minutes we are on, will be int datatypes
    hours = next_interval.hour
    minutes = next_interval.minute

    # turn the whole thing into minutes and divide by 30
    step_index = (hours * 60 + minutes) // 30

    print(f"Time interval we will be working with is: {next_interval}")
    print(f"step we are on out of 47: {step_index}")

    return step_index