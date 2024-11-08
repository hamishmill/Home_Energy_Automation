import random
import numpy as np
from .get_reward_script import get_reward

def train_q_table(num_episodes, starting_period, time_periods,gamma, epsilon_min, epsilon_start, alpha_min, alpha_start, decay_rate, actions, q_table
                  , solar_forecast, house_demand, max_battery_capacity, interval_C_rate, battery_capacity):
    #Q - Learning part
    for episode in range(num_episodes):  # Number of episodes

        current_battery_capacity = battery_capacity
        current_battery_level = battery_capacity/20

        for time in range(starting_period, time_periods): # loop over each hour

            useful_charge = 0
            excess_charge = 0

            epsilon = epsilon_min + (epsilon_start - epsilon_min) * np.exp(-decay_rate * episode)
            alpha = alpha_min + (alpha_start - alpha_min) * np.exp(-decay_rate * episode)

            if random.uniform(0, 1) < epsilon:
                action = random.choice(actions)  # explore
            else:
                action = np.argmax(q_table[current_battery_capacity, time])  # use current max
        

            # Get solar availability and house demand for this hour
            solar_available = solar_forecast[time]
            house_used = house_demand[time]

            #first step is to alter the battery level based on the sun levels
            if solar_available > house_used:
                potential_charge = solar_available - house_used
        
            # what can actually be used 
                useful_charge = min(potential_charge, max_battery_capacity - current_battery_level)

                excess_charge = potential_charge - useful_charge



            predicted_battery_level = current_battery_level + useful_charge
            #print(f'actoin chosen = {action}  predicted_battery_level after actions = {predicted_battery_level} and time = {time}')


            #new_battery_capacity = int(round((predicted_battery_level / 5) * 100))

            # Update battery level based on action
            if action == 0:  # Charge and power house from grid
             
                predicted_battery_level = min(max_battery_capacity, predicted_battery_level + interval_C_rate)

            elif action == 1:  # No battery charge, power house from grid
                pass

            elif action == 2:  # No battery charge and power house from battery if possible
                # here if solar is higher than house used then nothing will be changed 
                # if solar is less then we change the battery level to reflect we have powered the house via the battery
                if solar_available < house_used:
                    interval_drain =  house_used - solar_available
                    # caps the drain at 2.6 and makes sure battery stays above 0
                
                    if interval_drain >= interval_C_rate:
                        predicted_battery_level = max(0, predicted_battery_level - interval_C_rate) 
                    else:    
                        predicted_battery_level = max(0, predicted_battery_level - interval_drain) 
           

            #get the reward for this state and action
            reward = get_reward(time, current_battery_level, action, solar_forecast, house_demand, excess_charge)
        
        
            # gets the capacity for the state in the table this is after we have performed the action so is the next state
            new_battery_capacity = int(round((predicted_battery_level / max_battery_capacity) * 100))



            # next state is also the next time period
            next_time = (time + 1) % time_periods
            #get max value
            next_max = np.max(q_table[new_battery_capacity, next_time])

            # get the current states q-table value
            old_value = q_table[current_battery_capacity, time, action]

            #update it using the action reward, next state max and old value  (bellman equation)
            q_table[current_battery_capacity, time, action] = (1 - alpha) * old_value + alpha * (reward + gamma * next_max)


            #change to the new state,

            current_battery_capacity = new_battery_capacity
            current_battery_level = predicted_battery_level 
            time = next_time
    return q_table