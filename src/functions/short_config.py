# initialise parameters
#short config 

import numpy as np
import random
from get_battery_SOC import *
from get_time_script import *

# Parameters
def get_state():
    battery_SOC = get_battery_SOC()

    time = get_time_state()

    return time, battery_SOC

actions = [0,1,2]  # Possible actions involing charging and energy drain
time_periods = 48  # 24 hours in the day
max_battery_capacity = 5


battery_C_rate = 2.6   #kwh
interval_length = 24/time_periods   #length in hours
interval_C_rate = battery_C_rate * interval_length

#epsilon = 0.3  # Exploration rate
#alpha = 1  # Learning rate

#hyperparameters
gamma = 0.99  # Discount factor

epsilon_start = 1.0
epsilon_min = 0.1
alpha_start = 0.5
alpha_min = 0.05
decay_rate = 0.001

num_episodes = 10000

# q-table
def refresh_q_table():
    q_table = np.zeros((101, time_periods, len(actions)))

    return q_table