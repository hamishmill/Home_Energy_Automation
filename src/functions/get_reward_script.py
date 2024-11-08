def get_reward(time, battery_level, action, solar_forecast, house_demand, excess_charge, interval_C_rate,interval_length):
    """
    Returns the reward, which is then used to update the value for this state-action pair.

    Parameters:
        time (int): An integer between 0 and 23 representing the current hour.
        battery_level (int): Integer representing current battery charge between 0 and 100.
        action (int): Integer between 0-2 representing which action to take.
        solar_forecast (array): Forecasted solar energy for each hour of the day in kWh.
        house_demand (array): Forecasted power requirement of the house for each hour in kWh.

    Returns:
        float: Calculated reward for the given action and state.
        
    """
  
    # Define grid costs based on time of day
    if 2/interval_length <= time < 5/interval_length:  # Cheap charging hours (2-5 AM)
        grid_cost = 0.02
    elif 16/interval_length <= time < 19/interval_length:  # Expensive hours (4-7 PM)
        grid_cost = 0.32
    else:
        grid_cost = 0.23 # Normal hours

    # Get the power needed and solar availability for this specific hour 
    solar_available = solar_forecast[time]
    house_used = house_demand[time]

    # Calculate energy flows for the hour
    solar_used = min(solar_available, house_used)
    hourly_demand = house_used - solar_used

    
    #if when updating the battery there has been excess sun set a small penalty for the wasted sun
    reward = -excess_charge * 0.02

    # Reward Calculation
    if action == 0:  # Charge battery, power house from grid
        reward += -grid_cost * (hourly_demand + interval_C_rate)
    elif action == 1:  # No battery charge, power house from grid
        reward += -grid_cost * hourly_demand
    elif action == 2:  # No battery charge, power house from battery + grid if needed
    
        if hourly_demand >= interval_C_rate:  # hourly demand is higher than battery can provide
            reward -= (min(interval_C_rate, battery_level)) #* 0.01 + (hourly_demand - min(interval_C_rate, battery_level)) * grid_cost  # Small cost for using battery
        else:  # demand is low so potentially battey fully covers it 
        
            grid_needed = max((hourly_demand - min(interval_C_rate, battery_level)), 0)
            reward -= (grid_cost * grid_needed) #+ min(hourly_demand, battery_level ) * 0.01
            
        #penalise if not drained at the end
    if  time == 23 and battery_level > 0 :
         reward -= 2
    
    return reward