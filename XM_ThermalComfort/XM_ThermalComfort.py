#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
XM_ThermalComfort (Intelligent Heating Control based on Reinforcement Learning Techniques)
Copyright 2020 © Alberto Castellini, Alessandro Farinelli, Riccardo Sartea, Maddalena Zuccotto 

This file is part of XM_ThermalComfort.
XM_ThermalComfort is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

XM_ThermalComfort is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with XM.  If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>.

Please, report suggestions/comments/bugs to
alberto.castellini@univr.it, alessandro.farinelli@univr.it
"""


import numpy as np
import itertools
import pandas as pd
import sys
import os
from scipy.sparse import csr_matrix, issparse
from sklearn.metrics import mean_squared_error
import time
import datetime
from datetime import timedelta


dataset_dir = "dataset/"
results_dir = "results/"

try:
    t_des = pd.read_csv(os.path.join(dataset_dir, "thermal_profile.csv"), header=None).to_numpy()
    t_des = (np.round((t_des)*2)/2).astype(np.float32)
except FileNotFoundError:
    print("Thermal profile not found. Stopping...")
    exit(1)
except Exception:
    print("Error while reading thermal profile data. Stopping...")
    exit(1)

min_t_int = -20.
max_t_int = 50.

min_t_ext = -20.
max_t_ext = 50.

enrg = 0. # energy units

t_ints = {np.around(v, decimals=1): n for n, v in enumerate(np.arange(min_t_int, max_t_int, 0.5))}
t_exts = {np.around(v, decimals=1): n for n, v in enumerate(np.arange(min_t_ext, max_t_ext, 0.5))}
num_states = 7 * 24 * len(t_ints) * len(t_exts) 
num_actions = 2


# Positional notation parameters
p_t_ext = len(t_exts)
p_t_int = p_t_ext * len(t_ints)
p_hou = p_t_int * 24
p_day = p_hou * 7



# Finite Horizon
# Input:
#   T: transition probability matrix
#   R: reward matrix
#   discount: discount value
#   horizon: horizon value
# Output: 
#   Q.argmax(axis=0): policy time step 1 (0 (zero) if you start counting from 0)
def FH(T, R, discount, horizon):
    def rvec(r, t):
        if issparse(r):
            return r.multiply(t).sum(axis=1).A.reshape(num_states)
        elif issparse(t):
            return t.multiply(r).sum(axis=1).A.reshape(num_states)
        return np.multiply(r, t).sum(axis=1).A.reshape(num_states)

    Q = np.empty((num_actions, num_states))
    v = np.zeros(num_states) 
    R = tuple(map(rvec, R, T))

    for _ in range(horizon):
        for a in range(num_actions):
            Q[a] = R[a] + discount * T[a].dot(v)
        v = Q.max(axis=0)
    return Q.argmax(axis=0)  



# Calculate state index
# Input:
#   s: state
# Output: 
#   t_ext + t_int * p_t_ext + h * p_t_int + d * p_hou: state index expressed by positional notation
def state_index(s):
    # [days, hours, t_int, t_ext]
    if min_t_ext <= s[3] < max_t_ext and min_t_int <= s[2] < max_t_int and 0 <= s[1] <= 23 and 0 <= s[0] <= 6:
        t_ext = t_exts[s[3]]
        t_int = t_ints[s[2]]
        h = s[1]
        d = s[0]
        return t_ext + t_int * p_t_ext + h * p_t_int + d * p_hou
    return -1



# Compute reward
# Input:
#  s: state
#  a: action
# Output:
#   Reward
def compute_reward(s, a):
    return -((s[2] - t_des[s[0], s[1]])**2) - a * enrg



# Creation of transition probability matrix and reward matrix
# Input:
#   actions: 0, 1 (heater off, heater on)
#   k_b: heat dispersion coefficient of the building
#   k_h: coefficient which relates the heat produced by the heater to the temperature in the building
# Output: 
#   p_trans_mtx: transition probability matrix
#   reward_mtx: reward matrix
def MDP_matrix(actions, k_b, k_h):
    p_trans_mtx = [None, None]
    reward_mtx = [None, None]

    days = list(range(0,7))
    hours = list(range(0,24))

    var_lists = [days, hours, t_ints.keys(), t_exts.keys()]

    for a in actions:
        c = 0
        rows = np.zeros(num_states, dtype=np.int32)
        cols = np.zeros(num_states, dtype=np.int32)
        valsp = np.zeros(num_states, dtype=np.int8)
        valsr = np.zeros(num_states, dtype=np.float32)

        for s in itertools.product(*var_lists):
            s_index = state_index(s)

            next_s = [0, 0, 0, 0] # day, hour, int. temp, ext. temp. (next state)
            if (s[0] == 6 and s[1] == 23):
                next_s[0] = 0
                next_s[1] = 0  
            elif (s[1] == 23):
                next_s[0] = s[0]+1
                next_s[1] = 0
            else:
                next_s[0] = s[0]
                next_s[1] = s[1]+1
            
            next_s[2] = (np.round(M_environment(s[3], s[2], a, k_b, k_h)*2)/2).astype(np.float32)
            next_s[3] = s[3]

            next_s_index = state_index(next_s)

            if next_s_index != -1:
                rows[c] = s_index
                cols[c] = next_s_index
                valsp[c] = 1
                reward = compute_reward(next_s, a)
                # from state s, with action a, the system moves to next_s obtaining a reward
                valsr[c] = reward
            else:
                next_s[2] = s[2]
                next_s_index = state_index(next_s)
                rows[c] = s_index
                cols[c] = next_s_index
                valsp[c] = 1
                reward = compute_reward(next_s, a)
                valsr[c] = reward
            
            c += 1

        p_trans_mtx[a] = csr_matrix((valsp, (rows, cols)), shape=(num_states, num_states))
        reward_mtx[a] = csr_matrix((valsr, (rows, cols)), shape=(num_states, num_states))
    
    return p_trans_mtx, reward_mtx



# Model of the environment
# Input:
#   T_ext_i: external temperature at time i
#   T_int_i: internal stemperature at time i
#   C_i: heater state at time i
#   k_b: heat dispersion coefficient of the building
#   k_h: coefficient wich relates the heat produced by the heater to the temperature in the building
# Output:
#   T_int_i1: internal temperature at time i+1
def M_environment(T_ext_i, T_int_i, C_i, k_b, k_h):
    delta_T =(T_ext_i - T_int_i) * k_b + C_i * k_h
    T_int_i1 = T_int_i + delta_T
    return T_int_i1



# Find best adaptive params
# Input:
#   T_ext_oss: external temperatures in last 24 hrs
#   C_oss: heater states in last 24 hrs
#   T_int_oss: internal temperatures n last 24 hrs
# Output: 
#   best_k_b: NEW heat dispersion coefficient of the building
#   best_k_h: NEW coefficient wich relates the heat produced by the heater to the temperature in the building
def adaptive_params(T_ext_oss, C_oss, T_int_oss):
    k_b_list = []
    k_h_list = []
    
    dt_RealHouse = []
    for t_real in range(23):
        dt_RealHouse.append(T_int_oss[t_real+1] - T_int_oss[t_real])

    for b in np.arange(0.01, 0.11, 0.01): # from 0.01 to 0.1 with step 0.01
        k_b_list.append(np.around(b, decimals=2))
    for h in np.arange(1.0, 3.1, 0.2): # from 1 to 3 with step 0.2
        k_h_list.append(np.around(h, decimals=1))
    
    k_lists = [k_b_list, k_h_list]
    # determine every possible couple of values for k_b e k_h
    params_list = list(itertools.product(*k_lists))
    
    min_mse = float("inf")
    min_pos = -1
    
    # find the best couple k_b and k_h to model the environment comparing them with observated data
    for kk in range(len(params_list)):
        dt_params = [0]*23
        for x in range(23):
            # use of the model of the enviroment to predict the next internal temperature
            T_int_i = M_environment(T_ext_oss[x], T_int_oss[x], C_oss[x], params_list[kk][0], params_list[kk][1])
            dt_params[x] = T_int_i - T_int_oss[x]
        
        mse_error = mean_squared_error(dt_RealHouse, dt_params)
        
        if mse_error < min_mse:
            min_mse = mse_error
            min_pos = kk

    best_k_b = params_list[min_pos][0]
    best_k_h = params_list[min_pos][1]
    
    return best_k_b, best_k_h



# Controller
# Input:
#   policy: policy of MDP
#   date_time_file: datetime read from input file
#   t_ext_file: external temperature read from input file
#   t_int_file: internal temperature read from input file
#   k_b: heat dispersion coefficient of the building
#   k_h: coefficient wich relates the heat produced by the heater to the temperature in the building
# Output:
#   hcs: signal for the heating system
def M_controller(policy, date_time_file, t_ext_file, t_int_file, k_b, k_h):
    
    state_s = [0, 0, 0, 0] # day, hour, int. temp., ext. temp.

    state_s[0] = date_time_file.weekday()
    state_s[1] = date_time_file.hour
    state_s[2] = (np.round((t_int_file)*2)/2).astype(np.float32)
    state_s[3] = (np.round((t_ext_file)*2)/2).astype(np.float32)
    
    state_s_index = state_index(state_s)

    if state_s_index != -1:
        hcs = policy[state_s_index]
    else:
        hcs = -1

    return hcs



# Read sensor data
# Input:
#   expected_datetime: datetime from the system to check the presence of needed data
# Output:
#   date_time_file: sensor datetime for observed data
#   temp_ext_file: external temperature given by a sensor
#   temp_int_file: internal temperature given by a sensor
def read_observations(expected_datetime):
    
    data_waiting = 1
    c = 0
    while (data_waiting == 1):
        # Check existence of input data
        try:
            with open(os.path.join(dataset_dir, "sensor_data.csv"), "r") as observ:
            
                for line in observ:
                    splitted_line=line.split(",")
                    date_time_file = datetime.datetime.strptime(splitted_line[0], '%Y-%m-%d %H:%M:%S')
                    datetime_file_0m0s = date_time_file.replace(minute=0, second=0, microsecond=0)
                    expected_datetime = expected_datetime.replace(minute=0, second=0, microsecond=0)
                    
                    # If the needed observation is in the in the input file, memorize the observations
                    if (expected_datetime == datetime_file_0m0s):
                        data_waiting = 0
                        temp_ext_file = float(splitted_line[1])
                        temp_int_file = splitted_line[2]

                        if temp_int_file[:-2] == "\n":
                            temp_int_file = temp_int_file[:-2]
                    # Wait for the data at least for 4 minutes, checking every 1 minutes if data are available
                    else:
                        c +=1
                        if c == 5:
                            print("Sensor data not available for 4 minutes. Stopping...")
                            exit(1)
                        time.sleep(60)
                    break

        except FileNotFoundError:
            print("Sensor data not found. Stopping...")
            exit(1)
        except Exception:
            print("Error while reading sensor data. Stopping...")
            exit(1)

    return date_time_file, temp_ext_file, float(temp_int_file)
    


def main():

    actions = [0,1] # actions: 0 heating system off, 1 heating system on
    disc_fact = .6 # discount factor
    horiz = 7 # horizon
    
    k_b = 0.01 # init value
    k_h = 1. # init value
    
    recompute = True
    first_start = 1
    
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
    
    start_next_datetime = datetime.datetime.today()
    
    while(True):
    
        hcs_array=[]
        t_ext_arr = []
        t_int_arr = []

        if recompute:
            P_mtx, R_mtx = MDP_matrix(actions, k_b, k_h)
                                    
            policy = FH(P_mtx, R_mtx, disc_fact, horiz)
            
        for _ in range(24): # for to collect 24 hours of data to determine adaptive params

            now_datetime = datetime.datetime.today()
            if first_start == 0:
                time_to_wait = start_next_datetime - now_datetime
                time.sleep((time_to_wait).total_seconds()) # Wait one hour before reading again the input file

            date_time_csv, temp_ext_csv, temp_int_csv = read_observations(start_next_datetime)
            heater_signal = M_controller(policy, date_time_csv, temp_ext_csv, temp_int_csv, k_b, k_h)
            
            with open(os.path.join(results_dir, "heater_signal.csv"), "w") as out_signal:
                out_signal.write(str(heater_signal))

            hcs_array.append(heater_signal)
            t_ext_arr.append(temp_ext_csv)
            t_int_arr.append(temp_int_csv)
            
            first_start = 0
            start_next_datetime = start_next_datetime + timedelta(hours=1)
            
        k_b_new, k_h_new = adaptive_params(t_ext_arr, hcs_array, t_int_arr)
            
        if k_b != k_b_new or k_h != k_h_new:
            recompute = True
        else:
            recompute = False
       
        k_b = k_b_new
        k_h = k_h_new
        


main()
