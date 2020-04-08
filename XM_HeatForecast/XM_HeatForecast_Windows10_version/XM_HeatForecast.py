#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
XM_HeatForecast - eXplainable Modeling for heat forecast
Copyright 2020 © Alberto Castellini, Alessandro Farinelli, Federico Bianchi, Francesco Masillo

This file is part of XM_HeatForecast.
XM_HeatForecast is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

XM_HeatForecast is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with XM_HeatForecast.  If not, see <http://www.gnu.org/licenses/>.

Please, report suggestions/comments/bugs to
 alberto.castellini@univr.it, alessandro.farinelli@univr.it, federico.bianchi@univr.it, francesco.masillo@studenti.univr.it
"""
############################################################################### 

################################ LIBRARIES #################################### 

import sys

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

try:
    import ttk
    py3 = False
except ImportError:
    import tkinter.ttk as ttk
    py3 = True

import gui_support
import matplotlib.pyplot as plt

from tkinter import Tk, Frame, Menu, X, Y, TOP, BOTTOM, RIGHT, LEFT, BOTH, Listbox, Radiobutton, Button, OptionMenu, Label, Text, Canvas, Toplevel, StringVar, INSERT, END, VERTICAL, N, S, W, E, messagebox
from tkinter import filedialog
from datetime import datetime, timedelta
from sklearn.metrics import mean_squared_error
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from LoadingScreen import Splash


import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import pandas as pd
import numpy as np
# Schedule jobs
from apscheduler.schedulers.background import BackgroundScheduler
# Load model and Save model
import statsmodels.api as sm
# Calendar
#from workalendar.europe import Italy
import holidays
# Utils
import time
import copy
import glob, os, os.path, shutil, stat
from shutil import copyfile
from os import listdir
from os.path import isfile, join
from math import sqrt


############################################################################### 

############################### PARAMETERS #################################### 

# Forecast horizon
horizon = 0
# Mode
mode='demo'
# Features
features = ['day', 't', 'rh', 'ws', 'wd', 'r', 'h', 'l1', 'l2', 'l3', 'l4', 'l5',\
            'l6', 'l7', 'lp', 't2', 'tmv', 'tm', 'tm2', 'tmy', 'tmy2']

features_c = ['day', 'const','t', 'rh', 'ws', 'wd', 'r', 'h', 'l1', 'l2', 'l3', 'l4', 'l5',\
            'l6', 'l7', 'lp', 't2', 'tmv', 'tm', 'tm2', 'tmy', 'tmy2']
current_date = ''
new_iter = ''
results = []
model = ''
loads = ''

# Flags
switch = True
start = False
hours = 0

# Scheduler configuration  
scheduler = BackgroundScheduler()

############################################################################### 

############################### FUNCTIONS ##################################### 
############################### Forecaster #################################### 

# Gets permission
def get_perm(fname):
    return stat.S_IMODE(os.lstat(fname)[stat.ST_MODE])


# Changes permissions
def make_writeable_recursive(path):
    for root, dirs, files in os.walk(path, topdown=False):
        for dir in [os.path.join(root, d) for d in dirs]:
            os.chmod(dir, get_perm(dir) | os.ST_WRITE)
        for file in [os.path.join(root, f) for f in files]:
            os.chmod(file, get_perm(file) | os.ST_WRITE)

            
# Returns the current date
def dates():

    dates = pd.read_csv('Runtime/date.csv', index_col=0)
    dates['day'] = pd.to_datetime(dates['day'])
    
    return dates.loc[0, 'day'] 

            
# Cleans and sets directories
def utils():

   make_writeable_recursive('XM_HeatForecast')
           
   shutil.rmtree('Runtime')
   shutil.rmtree('Performance')
   shutil.rmtree('Forecast_files')
   shutil.rmtree('Model')


   os.mkdir('Runtime')       
   os.mkdir('Performance')  
   os.mkdir('Performance/Parameters')
   os.mkdir('Performance/Rsquared') 
   os.mkdir('Performance/Demo')   
   os.mkdir('Forecast_files')   
   os.mkdir('Model')
      
   rmse_demo = pd.DataFrame(data=None, columns=['day','avg_RMSE'])
   rmse_demo.to_csv('Performance/Demo/rmse_demo.csv')
   

# Weather forecasting
def weather_files():
    global horizon
    
    os.mkdir('Runtime/Weather_forecast')

    data = pd.read_csv('Data/weather.csv', index_col=0)
    data.columns = ['day', 't', 'rh','ws','wd','r']
    data['day'] = pd.to_datetime(data['day'])
    
    for idx in range(len(data)-horizon):
        temp = data.loc[idx:idx+horizon-1,:].reset_index(drop=True)
        temp.to_csv('Runtime/Weather_forecast/forecast_from_%s.csv' %(str(data.loc[idx, 'day']).replace(':', '_')))
        
        
# Checks the input
def evaluation(horizon):
    if(horizon != '24' and horizon != '48'):
        return False
    else:
        return True

    
# Sets the forecasting horizon
def forecasting_horizon(prompt=''):
    global horizon
    
    frame = tk.Tk()
    frame.geometry('300x50')
    frame.title('XM_HeatForecast')
    frame.resizable(0, 0)
    tk.Label(frame, text=prompt).pack()
    entry = tk.Entry(frame)
    entry.pack()    
    horizon = 48
    
    def callback(event):
        global horizon
        
        horizon = entry.get()
        if(evaluation(horizon)):
            frame.destroy()
        else:
            frame.destroy()
            forecasting_horizon('Enter Forecasting horizon (24h or 48h):')
    
    entry.bind("<Return>", callback)
    frame.mainloop()
    return int(horizon)


# Updates vector of dates
def update_dates():
# TODO
    dates = pd.read_csv('Runtime/date.csv', index_col=0)
    dates['day'] = pd.to_datetime(dates['day'])    
    dates = dates.loc[1:]
    dates.reset_index(inplace=True, drop=True)
    dates.to_csv('Runtime/date.csv')

    return


# MAIN MODULE
def forecast_module():

    global hours
    global current_date
    global new_iter
    global results
    global model
    global loads
    
    current_date = dates()
    update_dates()
        
    if(hours == 0):
        new_iter = copy.deepcopy(current_date)
        
    print('Forecasting the next %i hours, starting from %s' %(horizon,current_date))
    
    #if(datetime.datetime.now().hour == 0):
    if(current_date.hour == 0):
        print('Training model...')
        start = time.time()
        training_models(current_date)
        model = load_model(current_date)
        parameters_demo(model, current_date)
        rsquared(model, current_date)
        end = time.time()
        print('[%.1f ms] - Model is trained\n' %(1000 * (end - start)))
    
    
    print('Getting new data...')
    start = time.time()
    new_data = weather_forecast(current_date)
    end = time.time()
    print('[%.1f ms] - Data is downloaded\n' %(1000 * (end - start)))
    
    
    print('Processing data...')
    start = time.time()
    data = process_data(new_data, current_date)
    end = time.time()
    print('[%.1f ms] - Data is ready\n' %(1000 * (end - start)))
    
    
    print('Forecasting...')
    start = time.time()
    results = forecasting(model, data)
    if(mode == 'demo'):
        df = pd.DataFrame()
        df[['day', 'l']] = loads.loc[pd.to_datetime(loads['day']) >= current_date, :]
        df.reset_index(inplace=True, drop=True)
        df = df.loc[:horizon-1,:] 
        df['pred'] = results['pred']
        df.to_csv('Forecast_files/forecast_from_%s.csv' %(str(current_date).replace(':', '_')))

    else:
        results.to_csv('Forecast_files/forecast_from_%s.csv' %(str(current_date).replace(':', '_')))
    #results.to_csv('Forecast_files/forecast_from_%s.csv' %(pd.to_datetime(datetime.datetime.now().strftime('%Y-%m-%d %H:00:00'))))
    end = time.time()
    print('[%.1f ms] - Results are ready\n' %(1000 * (end - start)))
    
    update_data(current_date)
    print('Data is updated.\n\n\n')
    
    if(hours == horizon - 1):
        metrics(new_iter)
        hours = 0            
    else:
        hours += 1
    
    global startOn
    if startOn == True:
        print("Updating GUI")
        global top
        top.updateGUI()
        global toUpdate
        toUpdate = True
             
def training_models(current_date):
    
    X_dict = {} 
    y_dict = {}
    
    hist_data = pd.read_csv('Runtime/data.csv', index_col=0)
    hist_data.columns = features
    hist_data['day'] = pd.to_datetime(hist_data['day'])
    hist_data.reset_index(inplace=True, drop=True)
    
    hist_load = pd.read_csv('Runtime/load.csv', index_col=0)
    hist_load.columns = ['day', 'l']
    hist_load['day'] = pd.to_datetime(hist_load['day'])
    hist_load.reset_index(inplace=True, drop=True)  
    
    X_dict, y_dict = create_hourly_data(hist_data, hist_load) 
    create_hourly_model(X_dict, y_dict, current_date)


# Fits and saves model
def create_hourly_model(X_dict, y_dict,current_date):
    
    os.mkdir('Model/model_of_%s' %str(current_date).replace(':', '_'))
            
    for day in range(7):
        for hour in range(24):
            x1 = X_dict[day][hour].loc[:, 't':]
            if(x1.empty != True):
                y1 = y_dict[day][hour]['l']
                x1 = sm.add_constant(x1, has_constant='add')
                model = sm.OLS(y1.astype(float), x1.astype(float), hasconst=True).fit()               
                model.save('Model/model_of_%s/day_%i_hour_%i.pickle' %(str(current_date).replace(':', '_'), day, hour))


# Data processing                    
def create_hourly_data(hist_data, hist_load):
        
    Xd = {}
    yd = {}
    for day in range(7):
        Xd[day] = {}
        yd[day] = {}
        
    for day in range(7):
        for hour in range(24):
            Xd[day][hour] = hist_data.loc[np.logical_and(hist_data['day'].dt.weekday == day, hist_data['day'].dt.hour == hour), :]
            yd[day][hour] = hist_load.loc[np.logical_and(hist_load['day'].dt.weekday == day, hist_load['day'].dt.hour == hour), :]
       
        
    return Xd, yd


# Loads the model
def load_model(current_date):
    
    models = pd.DataFrame(data=None, columns=range(7), index=range(24))
        
    for cols in range(7):
        for rows in range(24):
            models.loc[rows, cols] = sm.load('Model/model_of_%s/day_%i_hour_%i.pickle' %(str(current_date).replace(':', '_'),cols,rows))               

    return models


# Gets model paramters
def parameters_demo(model, current_dt):
    
    dictionary = {}
    avg_dictionary = {}    
    for x in features_c[1:]:
        dictionary[x] = pd.DataFrame(data=None, index=range(24), columns=range(7))
        avg_dictionary[x] = pd.DataFrame(data=None, index=range(1), columns=range(7))
    
    for x in features_c[1:]:
        for day in range(7):
            for hour in range(24):
                dictionary[x].loc[hour, day] = model.loc[hour,day].params[x]
    
    for x in features_c[1:]:
        for day in range(7):
            avg_dictionary[x][day] = dictionary[x][day].mean()
            
    print(current_dt)
    os.mkdir('Performance/Parameters/from_%s' %str(current_dt).replace(':', '_'))
    
    os.mkdir('Performance/Parameters/from_%s/full_representation' %str(current_dt).replace(':', '_'))
    
    for x in features_c[1:]:
        avg_dictionary[x].to_csv('Performance/Parameters/from_%s/%s_from_%s.csv' %((str(current_dt)).replace(':', '_'), x, (str(current_dt)).replace(':', '_')))
        os.mkdir('Performance/Parameters/from_%s/full_representation/%s' %(str(current_dt).replace(':', '_'), x))
        dictionary[x].to_csv('Performance/Parameters/from_%s/full_representation/%s/%s_from_%s.csv' %(str(current_dt).replace(':', '_'), x, x, str(current_dt).replace(':', '_')))
        

# Gets Rsquared
def rsquared(model, current_dt):
    
    df = pd.DataFrame(data=None, columns=range(7), index=range(24))
    
    for hour in range(24):
        for day in range(7):
            df.loc[hour,day] = model.loc[hour, day].rsquared
    
    os.mkdir('Performance/Rsquared/%s' %str(current_dt).replace(':', '_'))
    
    df.to_csv('Performance/Rsquared/%s/rsquared.csv' %str(current_dt).replace(':', '_'))


# Returns the last weather forecasting
def weather_forecast(dt):    
   
   df = pd.read_csv('Runtime/Weather_forecast/forecast_from_%s.csv' %str(dt).replace(':', '_'), index_col=0)
   df['day'] = pd.to_datetime(df['day'])
   
   return df


# Processes new data
def process_data(new_data, current_date):
    
    hist_data = past_data()
    data = compute_new_features(hist_data, new_data,current_date)
        
    return data


# Loads the last 7 days data
def past_data():
        
    old_data = pd.read_csv('Runtime/data.csv', index_col=0)
    old_data.columns = features
    old_data['day'] = pd.to_datetime(old_data['day'])
    old_data.reset_index(inplace=True, drop=True)
    
    return old_data.tail(168)


# Features computation
def compute_new_features(hist_data, new_data,current_date):
    
    df = temp_derivation(hist_data, new_data)
    df = set_holidays(df)
    df = past_load(df,current_date)
    
    return df


# Temperature's features computation
def temp_derivation(hist_data, data):

    days = len(data['day']) // 24

    
    data['t2'] = pd.Series(0, index=data.index)
    data.loc[:,'t2'] = data.loc[:,'t']**2

       
    data['tm'] = pd.Series(0, index=data.index)   
    for x in range(days):
        for y in range(24*x, 24*(x + 1)):
            data.loc[y, 'tm'] = max(data.loc[24*x : 24*(x + 1), 't'])
    
    
    data['tm2'] = pd.Series(0, index=data.index)
    data.loc[:,'tm2'] = data.loc[:, 'tm']**2      

    
    comb = pd.concat([hist_data, data], sort=False)
    comb.reset_index(inplace=True, drop=True)

    
    comb.loc[168:, 'tmv'] = (comb['t'].rolling(169).mean())[168:]
    

    comb.loc[168:,'tmy'] = (comb['tm'].shift(24))[144:]
    comb.loc[168:,'tmy2'] = comb.loc[168:,'tmy']**2
      
    
    return comb       


# Holiday feature computation
def set_holidays(data):
    
    holidays_list = [x[0] for x in holidays.Italy(years = data.loc[0,'day'].year).items()]
            
    data['h'] = pd.Series(0, index=data.index)
    
    for hol in holidays_list:
        data.loc[data['day'].dt.date == holidays_list[0], 'h'] = 1
                
    return data   


# Past load features computation                
def past_load(data,current_date):

    load = pd.read_csv('Runtime/load.csv', index_col=0)
    load.reset_index(inplace=True, drop=True)
    real_load = pd.read_csv('Data/data.csv', index_col=0)
    real_load = real_load.loc[pd.to_datetime(real_load['day']) >= pd.to_datetime(current_date), ['day','lp']]
    real_load.reset_index(inplace=True, drop=True)
    real_load = real_load.loc[:horizon-1,:]
    
    data.loc[168:168+horizon-1, 'l1'] = load.tail(horizon)['l'].values
    data.loc[168:168+horizon-1, 'lp'] = real_load.loc[:,'lp'].values
    
    for lag in range(2,8):
        data.loc[len(data)-horizon:len(data)-1, 'l%i' %lag] = data.loc[len(data)-2*horizon:len(data)-horizon-1, 'l%i' %(lag-1)].values
           
    return data


# Forecasting function
def forecasting(model, data):
    
    global horizon
    results = pd.DataFrame(data=None, columns=['day', 'pred'])
       
    if (horizon <= 24):
        temp_data = copy.deepcopy(data)
        temp_data.insert(1, 'const', 1)

        results = pd.DataFrame(data=None, columns=['day', 'pred'])
        
        for idx in range(168, len(temp_data)):
            results.loc[idx, 'day'] = temp_data.loc[idx, 'day']
            results.loc[idx, 'pred'] = model.loc[temp_data.loc[idx, 'day'].hour][temp_data.loc[idx, 'day'].weekday()].predict(temp_data.loc[idx, 'const':].values)[0]
        
        results.reset_index(inplace=True, drop=True)
            
    elif(horizon > 24 and horizon <= 48):
        iteration = 0
        temp_data = copy.deepcopy(data.iloc[:168])
        temp_data.insert(1, 'const', 1)

        for idx in range(168):
            
            if(iteration + 1 <= 24):
                temp_data.loc[idx + 168, :] = data.loc[idx + 168, :]
                temp_data.loc[idx + 168, 'const'] = 1
    
                results.loc[idx, 'day'] = temp_data.loc[idx + 168, 'day']
                results.loc[idx, 'pred'] = (model.loc[temp_data.loc[idx + 168, 'day'].hour][temp_data.loc[idx + 168, 'day'].weekday()].predict(temp_data.loc[idx + 168, 'const':].values))[0] 
                iteration += 1
                
            elif(iteration + 1 > 24 and iteration + 1 <= 48):
                temp_data.loc[idx + 168, :] = data.loc[idx + 168, :]
                temp_data.loc[idx + 168, 'const'] = 1

                results.loc[idx, 'day'] = temp_data.loc[idx + 168, 'day']

                temp_data.loc[idx + 168, 'l1'] = results.loc[idx-24, 'pred']               
 
                offset = find(temp_data.loc[idx + 168, 'day'])
                    
                temp_data.loc[idx + 168, 'lp'] = data.loc[idx+168-offset, 'lp']                

                results.loc[idx, 'pred'] = (model.loc[temp_data.loc[idx + 168, 'day'].hour][temp_data.loc[idx + 168, 'day'].weekday()].predict(temp_data.loc[idx + 168, 'const':].values))[0] 
                results.reset_index(inplace=True, drop=True)
                iteration += 1
        
    return results


# Finds the hour of peak
def find(n):
        
    hour = n.hour
        
    if(hour > 6):
        remain = hour - 6
        result = 24 + remain
    elif(hour < 6):
        remain = 6 - hour
        result = 24 - remain 
    else:
        result = 24
            
    return result


# Updates data
def update_data(dt):

    old_data = pd.read_csv('Data/data.csv', index_col=0)
    old_data.columns = features
    old_data['day'] = pd.to_datetime(old_data['day'])
    
    old_load = pd.read_csv('Data/load.csv', index_col=0)
    old_load.columns = ['day', 'l']    
    old_load['day'] = pd.to_datetime(old_load['day'])

    
    old_data.loc[:old_data.loc[old_data['day'] == dt, :].index[0], :].to_csv('Runtime/data.csv')
    old_load.loc[:old_load.loc[old_load['day'] == dt, :].index[0], :].to_csv('Runtime/load.csv')

    return


# Prepares data for metrics computation
def metrics(current_dt):
    
    if(mode == 'demo'):
        metrics_computation_demo(current_dt)
        

def metrics_computation_demo(current_dt):
    files = [f for f in listdir('Forecast_files') if isfile(join('Forecast_files', f))]
 
    files.sort(reverse=False)
        
    rmse_demo = pd.read_csv('Performance/Demo/rmse_demo.csv', index_col=0)
    
    rmse_evol = pd.DataFrame(data=None, columns=['RMSE'])
    
    iters = 0
    for file in files:
        df = pd.read_csv('Forecast_files/%s' %(file), index_col = 0)
        rmse_evol.loc[iters, 'RMSE'] = RMSE(df['l'], df['pred'])
              
    
    idx = len(rmse_demo)
    rmse_demo.loc[idx, 'day'] = current_dt
    rmse_demo.loc[idx, 'avg_RMSE'] = rmse_evol['RMSE'].mean()
    
    os.mkdir('Performance/Demo/%s' %(str(current_dt).replace(':', '_')))
    rmse_demo.to_csv('Performance/Demo/%s/rmse_demo.csv' %str(current_dt).replace(':', '_'))
    
    rmse_demo.to_csv('Performance/Demo/rmse_demo.csv')


# Computes the Root-Mean-Squared-Error metric
def RMSE(y_actual, y_predicted):
    
    y_predicted = pd.DataFrame({'res':y_predicted})
    y_predicted = pd.Series(y_predicted['res']) 

    return sqrt(mean_squared_error(y_actual, y_predicted))


def set_runtime_data(current_date):
    
    global loads
    global mode
    
    date = pd.read_csv('Data/date.csv', index_col=0)
    data = pd.read_csv('Data/data.csv', index_col=0)
    load = pd.read_csv('Data/load.csv', index_col=0)
    
    date = date.loc[pd.to_datetime(date['day']) >= current_date, :]
    date.reset_index(inplace=True, drop=True)
    
    data = data.loc[pd.to_datetime(data['day']) < current_date, :]
    data.reset_index(inplace=True, drop=True)    
    
    past_load = load.loc[pd.to_datetime(load['day']) < current_date, :]
    past_load.reset_index(inplace=True, drop=True)  
    
    next_load= load.loc[pd.to_datetime(load['day']) >= current_date, :]
    next_load.reset_index(inplace=True, drop=True)
    
    date.to_csv('Runtime/date.csv')
    data.to_csv('Runtime/data.csv')
    past_load.to_csv('Runtime/load.csv')
    next_load.to_csv('Runtime/next_load.csv')

    
    if(mode == 'demo'):
        loads = pd.read_csv('Runtime/next_load.csv', index_col=0)
        loads['day'] = pd.to_datetime(loads['day'])
    
    
def set_horizon(new_horizon):
    global horizon

    horizon = new_horizon    
    weather_files()


def set_refreshRate(t):
    global scheduler
    
    scheduler.add_job(forecast_module, 'interval', id='forecaster', seconds=t)


def set_date(date):
    global current_date
    
    current_date = pd.to_datetime(date)
    set_runtime_data(current_date)
    
    
    
################################ GUI ########################################## 


def vp_start_gui(pathDir):
    '''Starting point when module is the main routine.'''
    global val, w, root, top
    
    root = tk.Tk()
    img = tk.PhotoImage(file=pathDir+'/Imgs/XM.png')
    root.tk.call('wm', 'iconphoto', root._w, img)
    top = mainWindow (root, pathDir)
    #gui_support.init(root, top)
    root.protocol("WM_DELETE_WINDOW", destroy_mainWindow)
    root.mainloop()
    #return root

w = None
def create_mainWindow(root, *args, **kwargs):
    '''Starting point when module is imported by another program.'''
    global w, w_win, rt
    rt = root
    w = tk.Toplevel (root)
    top = mainWindow (w)
    gui_support.init(w, top, *args, **kwargs)
    return (w, top)

def destroy_mainWindow():
    import sys
    global scheduler
    
    global root, top
    if top._job is not None:
        top.root.after_cancel(top._job)
        top._job = None
    if len(scheduler.get_jobs()) > 0:
        scheduler.remove_job('forecaster')
    if scheduler.running:
        scheduler.shutdown()
    root.destroy()
    root = None
    print("\nExited\n")
    sys.exit()

class mainWindow:
    def __init__(self, top=None, pathDir=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        self.pathDir = pathDir
        #self.now = current_date#datetime.strptime(current_date, "%Y-%m-%d %H:%M:%S")
        #print(self.now)
        self.countDays = 0
        self.root = top.winfo_toplevel()
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85'
        _ana2color = '#ececec' # Closest X11 color: 'gray92'
        self.style = ttk.Style()
        if sys.platform == "win32":
            self.style.theme_use('winnative')
        self.style.configure('.',background=_bgcolor)
        self.style.configure('.',foreground=_fgcolor)
        self.style.configure('.',font="TkDefaultFont")
        self.style.map('.',background=
            [('selected', _compcolor), ('active',_ana2color)])

        top.geometry("600x477+412+146")
        top.state('zoomed')
        top.minsize(1, 1)
        #top.maxsize(1351, 738)
        top.resizable(1, 1)
        top.title("XM_HeatForecast")
        top.configure(highlightcolor="black")

        self.LabelDate = tk.Label(top)
        self.LabelDate.place(relx=0.40, rely=0.0063, height=25, width=299)
        self.LabelDate.configure(activebackground="#f9f9f9")
        self.LabelDate.configure(anchor='w')
        self.LabelDate.configure(text="Current time: ")#+str(self.now))
        
        self.ButtonStart = tk.Button(top)
        self.ButtonStart.place(relx=0.85, rely=0.008, height=25, width=60)
        self.ButtonStart.configure(text="Start", command=self.startStop)
        self.start = 0
        
        self.ButtonHelp = tk.Button(top)
        self.ButtonHelp.place(relx=0.923, rely=0.008, height=25, width=30)
        self.ButtonHelp.configure(text='''?''', command=self.showLegend)

        self.Frame48H = tk.Frame(top)
        self.Frame48H.place(relx=0.033, rely=0.063, relheight=0.43
                , relwidth=0.458)
        self.Frame48H.configure(relief='groove')
        self.Frame48H.configure(borderwidth="2")
        self.Frame48H.configure(relief="groove")

        self.Canvas48H = tk.Canvas(self.Frame48H)
        self.Canvas48H.place(relx=0.007, rely=0.005, relheight=0.98
                , relwidth=0.985)
        self.Canvas48H.configure(borderwidth="2")
        self.Canvas48H.configure(relief="ridge")
        self.Canvas48H.configure(selectbackground="#c4c4c4")
        self.fig48H = plt.figure()
        self.ax48H = self.fig48H.add_subplot(111)
        self.ax48HTwin = self.ax48H.twinx()
        self.ax48HTwin.axes.get_yaxis().set_visible(False)
        self.FigureCanvas48H = FigureCanvasTkAgg(self.fig48H, self.Canvas48H)
        self.addClickable(self.fig48H, 1)

        self.FrameSele48H = tk.Frame(top)
        self.FrameSele48H.place(relx=0.033, rely=0.013, relheight=0.052
                , relwidth=0.242)
        self.FrameSele48H.configure(relief='groove')
        self.FrameSele48H.configure(borderwidth="2")
        self.FrameSele48H.configure(relief='groove')

        self.LabelSele48H = tk.Label(self.FrameSele48H)
        #self.LabelSele48H.place(relx=0.015, rely=0.24, height=15, width=119)
        self.LabelSele48H.pack(side=LEFT)
        self.LabelSele48H.configure(anchor='w')
        self.LabelSele48H.configure(text='''Select variable:''')
        self.var48H = StringVar(self.FrameSele48H)
        self.options48H = ["None","t","rh","ws","wd","r"]
        self.var48H.set(self.options48H[0])
        self.optionMenu48H = OptionMenu(self.FrameSele48H, self.var48H, *self.options48H)
        self.optionMenu48H.pack(side=LEFT)
        self.updateSele48H = Button(self.FrameSele48H)
        self.updateSele48H.configure(text="Update", command=self.changeSele48H)
        self.updateSele48H.pack(side=LEFT)
        #self.draw48H()

        self.FrameLastEpoch = tk.Frame(top)
        self.FrameLastEpoch.place(relx=0.5, rely=0.063, relheight=0.43
                , relwidth=0.475)
        self.FrameLastEpoch.configure(relief='groove')
        self.FrameLastEpoch.configure(borderwidth="2")
        self.FrameLastEpoch.configure(relief="groove")

        self.CanvasLastEpoch = tk.Canvas(self.FrameLastEpoch)
        self.CanvasLastEpoch.place(relx=0.007, rely=0.005, relheight=0.98
                , relwidth=0.986)
        self.CanvasLastEpoch.configure(borderwidth="2")
        self.CanvasLastEpoch.configure(relief="ridge")
        self.CanvasLastEpoch.configure(selectbackground="#c4c4c4")
        self.figLastEpoch = plt.figure()
        self.axLastEpoch = self.figLastEpoch.add_subplot(111)
        self.axLastEpochTwin = self.axLastEpoch.twinx()
        self.FigureCanvasLastEpoch = FigureCanvasTkAgg(self.figLastEpoch, self.CanvasLastEpoch)
        self.addClickable(self.figLastEpoch, 2)
        #self.drawLastEpoch()

        self.TSeparator1 = ttk.Separator(top)
        self.TSeparator1.place(relx=0.023, rely=0.507, relwidth=0.95)
        
        self.FrameChoice = tk.Frame(top)
        self.FrameChoice.place(relx=0.033, rely=0.516, relheight=0.052
                , relwidth=0.458)
        self.FrameChoice.configure(relief='groove')
        self.FrameChoice.configure(borderwidth="2")
        self.FrameChoice.configure(relief="groove")
        self.varDayChoice = StringVar(self.FrameChoice)
        self.varHourChoice = StringVar(self.FrameChoice)
        self.varVarChoice = StringVar(self.FrameChoice)
        self.optionsDayChoice = ["All","Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
        self.varDayChoice.set(self.optionsDayChoice[0])
        self.optionsHourChoice = ["All","00","01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16","17","18","19","20","21","22","23"]
        self.varHourChoice.set(self.optionsHourChoice[0])
        self.optionsVarChoice = ["All","const","h","l1","l2","l3","l4","l5","l6","l7","lp","r","rh","t","t2","tm","tm2","tmv","tmy","tmy2","wd","ws"]
        self.varVarChoice.set(self.optionsVarChoice[0])
        self.optionMenuDayChoice = OptionMenu(self.FrameChoice, self.varDayChoice, *self.optionsDayChoice)
        self.optionMenuHourChoice = OptionMenu(self.FrameChoice, self.varHourChoice, *self.optionsHourChoice)
        self.optionMenuVarChoice = OptionMenu(self.FrameChoice, self.varVarChoice, *self.optionsVarChoice)
        self.LabelDays = Label(self.FrameChoice, text="Day(s):")
        self.LabelDays.pack(side=LEFT)
        self.optionMenuDayChoice.pack(side=LEFT)
        self.LabelHours = Label(self.FrameChoice, text="Hour(s):")
        self.LabelHours.pack(side=LEFT)
        self.optionMenuHourChoice.pack(side=LEFT)
        self.LabelVars = Label(self.FrameChoice, text="Var(s):")
        self.LabelVars.pack(side=LEFT)
        self.optionMenuVarChoice.pack(side=LEFT)
        self.updateChoice = Button(self.FrameChoice)
        self.updateChoice.configure(text="Update", command=self.drawChoice)
        self.updateChoice.pack(side=LEFT)
        
        self.FrameDisplayChoice = tk.Frame(top)
        self.FrameDisplayChoice.place(relx=0.033, rely=0.566, relheight=0.43
                , relwidth=0.458)
        self.FrameDisplayChoice.configure(relief='groove')
        self.FrameDisplayChoice.configure(borderwidth="2")
        self.FrameDisplayChoice.configure(relief="groove")
        #self.drawChoice()
        
        self.FrameTSSele = tk.Frame(top)
        self.FrameTSSele.place(relx=0.5, rely=0.516, relheight=0.052, relwidth=0.475)
        self.FrameTSSele.configure(relief='groove')
        self.FrameTSSele.configure(borderwidth="2")
        self.FrameTSSele.configure(relief="groove")
        self.varTS1 = StringVar(self.FrameTSSele)
        self.varTS2 = StringVar(self.FrameTSSele)
        self.optionsVarTS1 = ["None","h","l1","l2","l3","l4","l5","l6","l7","lp","r","rh","t","t2","tm","tm2","tmv","tmy","tmy2","wd","ws"]
        self.varTS1.set(self.optionsVarTS1[12])
        self.optionsVarTS2 = ["None","h","l1","l2","l3","l4","l5","l6","l7","lp","r","rh","t","t2","tm","tm2","tmv","tmy","tmy2","wd","ws"]
        self.varTS2.set(self.optionsVarTS2[14])
        self.optionMenuVarTS1 = OptionMenu(self.FrameTSSele, self.varTS1, *self.optionsVarTS1)
        self.LabelVarTS1 = Label(self.FrameTSSele, text="Var 1:")
        self.LabelVarTS1.pack(side=LEFT)
        self.optionMenuVarTS1.pack(side=LEFT)
        self.optionMenuVarTS2 = OptionMenu(self.FrameTSSele, self.varTS2, *self.optionsVarTS2)
        self.LabelVarTS2 = Label(self.FrameTSSele, text="Var 2:")
        self.LabelVarTS2.pack(side=LEFT)
        self.optionMenuVarTS2.pack(side=LEFT)
        self.updateVarTS = Button(self.FrameTSSele)
        self.updateVarTS.configure(text="Update", command=self.drawTS)
        self.updateVarTS.pack(side=LEFT)

        self.FrameTS = tk.Frame(top)
        self.FrameTS.place(relx=0.5, rely=0.566, relheight=0.43, relwidth=0.475)
        self.FrameTS.configure(relief='groove')
        self.FrameTS.configure(borderwidth="2")
        self.FrameTS.configure(relief="groove")
        
        self.CanvasTS = tk.Canvas(self.FrameTS)
        self.CanvasTS.place(relx=0.007, rely=0.005, relheight=0.98
                , relwidth=0.986)
        self.CanvasTS.configure(borderwidth="2")
        self.CanvasTS.configure(relief="ridge")
        self.CanvasTS.configure(selectbackground="#c4c4c4")
        self.figTS = plt.figure()
        self.axTS = self.figTS.add_subplot(111)
        self.axTSTwin = self.axTS.twinx()
        self.FigureCanvasTS = FigureCanvasTkAgg(self.figTS, self.CanvasTS)
        self.addClickable(self.figTS, 4)
        #self.drawTS()
        
        #self.updateGUI()
        global toUpdate
        toUpdate = False
        self._job = self.root.after(1000, self.refreshGUI)
        self.firstTime = True
        
    def startParameters(self):
        rootParam = Toplevel(self.root)
        imgP = tk.PhotoImage(file=self.pathDir+'/Imgs/XM.png')
        rootParam.tk.call('wm', 'iconphoto', rootParam._w, imgP)
        top = ParametersWindow(self, rootParam, self.pathDir)
        rootParam.protocol("WM_DELETE_WINDOW", top.cancel)
        rootParam.mainloop()    
    
    def refreshGUI(self):
        global toUpdate
        if toUpdate:
            self.FigureCanvas48H.draw()
            self.FigureCanvasLastEpoch.draw()
            self.FigureCanvasTS.draw()
            self.root.update()
            toUpdate = False
        self._job = self.root.after(1000, self.refreshGUI)
        
    def startStop(self):
        if self.start == 0:
            self.start = 1
            self.ButtonStart.configure(text="Stop")
            global startOn
            if startOn == False:
                self.startParameters()
            else:
                restart()
        else:
            self.start = 0
            self.ButtonStart.configure(text="Resume")
            switchoff()
        
    def changeSele48H(self, force=True):
        import pandas as pd
        
        if self.firstTime:
            return
        self.ax48HTwin.axes.get_yaxis().set_visible(False)
        if len(self.ax48HTwin.get_lines()) > 0:
            self.ax48HTwin.lines.pop(0)
        if self.var48H.get() != "None":
            self.ax48HTwin.axes.get_yaxis().set_visible(True)
            dataset = pd.read_csv(self.pathDir+"/Runtime/Weather_forecast/forecast_from_"+str(self.now).replace(':', '_')+".csv")#.strftime("%Y-%m-%d %H:%M:%S")
            self.ax48HTwin.plot(dataset[self.var48H.get()],c="r", label = self.var48H.get())
            self.ax48HTwin.relim()
            self.ax48HTwin.autoscale_view()
            self.ax48HTwin.set_ylabel(self.var48H.get(), fontsize=8)
            self.ax48HTwin.tick_params(axis='y', which='major', labelsize=8)
            lines = []
            labLines = []
            for line in self.ax48H.get_lines():
                lines.append(line)
                labLines.append(line.get_label())
            lines.append(self.ax48HTwin.get_lines()[0])
            labLines.append(self.ax48HTwin.get_lines()[0].get_label())
            self.ax48H.legend(lines, labLines)
        else:
            self.ax48H.legend()
        if force:
            self.FigureCanvas48H.draw()
            
    def draw48H(self):
        import pandas as pd
        import matplotlib.ticker as ticker
        from sklearn.metrics import mean_squared_error
        import math
        
        pathToUse = self.pathDir+"/Forecast_files/"
        dataset = pd.read_csv(pathToUse+"forecast_from_"+str(self.now).replace(':','_')+".csv")#.strftime("%Y-%m-%d %H:%M:%S")
        #self.fig48H.set_size_inches([self.Frame48H.winfo_width()/100, self.Frame48H.winfo_height()/100])
        self.ax48H.clear()
        self.ax48H.plot(dataset["day"], dataset["l"], label="True")
        self.ax48H.plot(dataset["day"], dataset["pred"], label="Pred")
        self.ax48H.xaxis.set_major_locator(ticker.AutoLocator())
        plt.setp(self.ax48H.xaxis.get_majorticklabels(),
         'rotation', 30, 'ha', "right", 'fontsize', 6)
        self.ax48H.set_ylabel("Heating load [MWh]", fontsize=8)
        self.ax48H.text(0.45, 0.85, "RMSE = {0:.2f}".format(math.sqrt(mean_squared_error(dataset["l"], dataset["pred"]))), transform=self.fig48H.transFigure);
        self.fig48H.subplots_adjust(top=0.90, bottom = 0.23, left=0.1, right = 0.90)
        self.ax48H.set_title("Heating load prediction for the next 48H", fontsize=10, fontweight='bold')
        self.ax48H.grid(True)
        self.ax48H.legend()
        self.FigureCanvas48H.get_tk_widget().pack(fill=BOTH, expand=1)
        #tool = NavigationToolbar2Tk(canvas, self.Frame48H)
        #tool.update()
        self.FigureCanvas48H._tkcanvas.pack(fill=BOTH, expand=1)
        self.ax48H.tick_params(axis='y', which='major', labelsize=8)
        #self.ax48H.set_yticklabels(self.ax48H.get_yticklabels(), fontsize='8')
        
    def drawLastEpoch(self):
        import os
        import pandas as pd
        import numpy as np
        import math
        #from sklearn.metrics import mean_squared_error
        import matplotlib.ticker as ticker
        from matplotlib.ticker import FormatStrFormatter
        
        if self.firstTime:
            return
        pathToUse = self.pathDir+"/Forecast_files/"
        self.rmse = []
        self.r2 = []
        self.days = []
        files = sorted(os.listdir(pathToUse))
        for fi in files:
            if fi > "forecast_from_"+str(self.now)+".csv":#.strftime("%Y-%m-%d %H:%M:%S")
                break
            dataset = pd.read_csv(pathToUse+fi)
            self.rmse.append(math.sqrt(mean_squared_error(dataset["l"], dataset["pred"])))
            self.days.append(dataset["day"].iloc[0])
            pastString = fi.split("_")[2].split(" ")[0]
            dataset = pd.read_csv(self.pathDir+"/Performance/Rsquared/"+pastString+" 00_00_00/rsquared.csv", index_col=0)
            self.r2.append(np.mean(dataset.values.ravel()))
        if len(self.rmse) > 2160:
            self.rmse = self.rmse[len(self.rmse)-2160:]
            self.r2 = self.r2[len(self.r2)-2160:]
        if len(self.rmse) == 1:
            self.scatter1 = self.axLastEpoch.scatter(self.days, self.rmse, label="RMSE")
            self.scatter2 = self.axLastEpochTwin.scatter(self.days, self.r2, c="orange", label="R^2")
        else:
            self.axLastEpoch.plot(self.days, self.rmse, label="RMSE")
            self.axLastEpochTwin.plot(self.days, self.r2, c="orange", label="R^2")
        self.axLastEpoch.set_ylabel("Root Mean Squared Error [MWh]", fontsize = 8)
        self.axLastEpochTwin.set_ylabel("R^2", fontsize=8)
        self.axLastEpoch.set_title("Model evaluation (RMSE and R^2)", fontsize=10, fontweight='bold')  
        self.axLastEpoch.xaxis.set_major_locator(ticker.AutoLocator())
        self.axLastEpoch.grid(True)
        """
        lns = self.axLastEpoch.get_lines()+self.axLastEpochTwin.get_lines()
        labelsLns = []
        for line in lns:
            labelsLns.append(line.get_label())
        plt.legend(lns, labelsLns)
        """
        plt.setp(self.axLastEpoch.xaxis.get_majorticklabels(),
         'rotation', 30, 'ha', "right", 'fontsize', 6)
        self.figLastEpoch.subplots_adjust(top=0.90, bottom = 0.23, left=0.12, right = 0.88)
        self.axLastEpoch.tick_params(axis='y', which='major', labelsize=8)
        self.axLastEpochTwin.tick_params(axis='y', which='major', labelsize=8)
        self.axLastEpochTwin.yaxis.set_major_formatter(FormatStrFormatter('%.4f'))
        self.FigureCanvasLastEpoch.get_tk_widget().pack(fill=BOTH, expand=1)
        #tool = NavigationToolbar2Tk(canvas, self.Frame48H)
        #tool.update()
        self.FigureCanvasLastEpoch._tkcanvas.pack(fill=BOTH, expand=1)
        
    def updateLastEpoch(self):
        import pandas as pd
        import numpy as np
        import math        
        #from sklearn.metrics import mean_squared_error
        import matplotlib.ticker as ticker
        from matplotlib.ticker import FormatStrFormatter
        
        if self.firstTime:
            return
        pathToUse = self.pathDir+"/Forecast_files/"
        dataset = pd.read_csv(pathToUse+"forecast_from_"+str(self.now).replace(':', '_')+".csv")#.strftime("%Y-%m-%d %H:%M:%S")
        self.rmse.append(math.sqrt(mean_squared_error(dataset["l"], dataset["pred"])))
        self.days.append(dataset["day"].iloc[0])
        dataset = pd.read_csv(self.pathDir+"/Performance/Rsquared/"+str(self.now).split(" ")[0]+" 00_00_00/rsquared.csv", index_col=0)#.strftime("%Y-%m-%d")
        self.r2.append(np.mean(dataset.values.ravel()))
        if len(self.rmse) > 2160:
            self.rmse = self.rmse[1:]
            self.days = self.days[1:]
            self.r2 = self.r2[1:]
        self.axLastEpoch.clear()
        self.axLastEpochTwin.clear()
        self.axLastEpoch.plot(self.days, self.rmse, label="RMSE")
        self.axLastEpoch.set_ylabel("Root Mean Squared Error [MWh]", fontsize = 8)
        self.axLastEpochTwin.plot(self.days, self.r2, c="orange", label="R^2")
        self.axLastEpochTwin.set_ylabel("R^2", fontsize=8)
        self.axLastEpoch.set_title("Model evaluation (RMSE and R^2)", fontsize=10, fontweight='bold')                  
        self.axLastEpoch.xaxis.set_major_locator(ticker.AutoLocator())
        self.axLastEpoch.grid(True)
        self.axLastEpoch.tick_params(axis='y', which='major', labelsize=8)
        self.axLastEpochTwin.tick_params(axis='y', which='major', labelsize=8)
        self.axLastEpochTwin.yaxis.set_major_formatter(FormatStrFormatter('%.4f'))
        lns = self.axLastEpoch.get_lines()+self.axLastEpochTwin.get_lines()
        labelsLns = []
        for line in lns:
            labelsLns.append(line.get_label())
        self.axLastEpoch.legend(lns, labelsLns)
        plt.setp(self.axLastEpoch.xaxis.get_majorticklabels(),
         'rotation', 30, 'ha', "right", 'fontsize', 6)
        self.figLastEpoch.subplots_adjust(top=0.90, bottom = 0.23, left=0.12, right = 0.88)
        #self.FigureCanvasLastEpoch.get_tk_widget().pack(fill=BOTH, expand=1)
        #tool = NavigationToolbar2Tk(canvas, self.Frame48H)
        #tool.update()
        #self.FigureCanvasLastEpoch._tkcanvas.pack(fill=BOTH, expand=1)
        #self.FigureCanvasLastEpoch.draw()
        #self.root.update()
        
    def getChoice(self):
        import pandas as pd
        
        flagDayAll = False
        flagHourAll = False
        flagVarAll = False
        if self.varDayChoice.get() != "All":
            dictDay = dict([(y,x) for x,y in enumerate(self.optionsDayChoice[1:])])
            dayToUse = dictDay[self.varDayChoice.get()]
        else:
            dayToUse = range(0,7)
            flagDayAll = True
        if self.varHourChoice.get() != "All":
            hourToUse = int(self.varHourChoice.get())
        else:
            hourToUse = range(0,24)
            flagHourAll = True
        if self.varVarChoice.get() != "All":
            varToUse = self.varVarChoice.get()
        else:
            varToUse = self.optionsVarChoice[1:]
            flagVarAll = True
        result = []
        if flagDayAll == True and flagHourAll == True and flagVarAll==True:
            for var in varToUse:
                pathToUse = self.pathDir+"/Performance/Parameters/from_"+str(self.now).split(" ")[0]+" 00_00_00/full_representation/"+var+"/"+var+"_from_"+str(self.now).split(" ")[0]+" 00_00_00.csv"
                dataset = pd.read_csv(pathToUse, index_col = 0)
                #print(list(dataset.iloc[:, :].values))
                result.append((dataset.values.ravel()))
        elif flagDayAll == True and flagHourAll == True and flagVarAll==False:
            pathToUse = self.pathDir+"/Performance/Parameters/from_"+str(self.now).split(" ")[0]+" 00_00_00/full_representation/"+varToUse+"/"+varToUse+"_from_"+self.now.strftime("%Y-%m-%d")+" 00_00_00.csv"
            dataset = pd.read_csv(pathToUse, index_col = 0)
            result = dataset.values
        elif flagDayAll == True and flagHourAll == False and flagVarAll==True:
            for var in varToUse:
                pathToUse = self.pathDir+"/Performance/Parameters/from_"+str(self.now).split(" ")[0]+" 00_00_00/full_representation/"+var+"/"+var+"_from_"+self.now.strftime("%Y-%m-%d")+" 00_00_00.csv"
                dataset = pd.read_csv(pathToUse, index_col = 0)
                result.append(dataset.iloc[hourToUse, :])
        elif flagDayAll == False and flagHourAll == True and flagVarAll==True:
            for var in varToUse:
                pathToUse = self.pathDir+"/Performance/Parameters/from_"+str(self.now).split(" ")[0]+" 00_00_00/full_representation/"+var+"/"+var+"_from_"+str(self.now).split(" ")[0]+" 00_00_00.csv"
                dataset = pd.read_csv(pathToUse, index_col = 0)
                result.append(dataset.iloc[:, dayToUse])
        elif flagDayAll == True and flagHourAll == False and flagVarAll==False:
            pathToUse = self.pathDir+"/Performance/Parameters/from_"+str(self.now).split(" ")[0]+" 00_00_00/full_representation/"+varToUse+"/"+varToUse+"_from_"+str(self.now).split(" ")[0]+" 00_00_00.csv"
            dataset = pd.read_csv(pathToUse, index_col = 0)
            result.extend(list(dataset.iloc[hourToUse, :]))
        elif flagDayAll == False and flagHourAll == True and flagVarAll==False:
            pathToUse = self.pathDir+"/Performance/Parameters/from_"+str(self.now).split(" ")[0]+" 00_00_00/full_representation/"+varToUse+"/"+varToUse+"_from_"+str(self.now).split(" ")[0]+" 00_00_00.csv"
            dataset = pd.read_csv(pathToUse, index_col = 0)
            result.extend(list(dataset.iloc[:, dayToUse]))
        elif flagDayAll == False and flagHourAll == False and flagVarAll==True:
            for var in varToUse:
                pathToUse = self.pathDir+"/Performance/Parameters/from_"+str(self.now).split(" ")[0]+" 00_00_00/full_representation/"+var+"/"+var+"_from_"+str(self.now).split(" ")[0]+" 00_00_00.csv"
                dataset = pd.read_csv(pathToUse, index_col = 0)
                result.append(dataset.iloc[hourToUse, dayToUse])
        if flagDayAll == False and flagHourAll == False and flagVarAll == False:
            pathToUse = self.pathDir+"/Performance/Parameters/from_"+str(self.now).split(" ")[0]+" 00_00_00/full_representation/"+varToUse+"/"+varToUse+"_from_"+str(self.now).split(" ")[0]+" 00_00_00.csv"
            dataset = pd.read_csv(pathToUse, index_col = 0)
            result = [dataset.iloc[hourToUse, dayToUse]]
        return result
    
    
    def drawChoice(self):
        import pandas as pd
        from pandastable import Table#, config
        
        if self.firstTime:
            return
        if len(self.FrameDisplayChoice.pack_slaves()) > 0:
            for slave in self.FrameDisplayChoice.pack_slaves():
                slave.destroy()
        result = self.getChoice()
        try:
            result = pd.DataFrame(result)
        except:
            pass
        if self.varDayChoice.get() == "All" and self.varHourChoice.get() == "All" and self.varVarChoice.get() == "All":
            fig = plt.figure(figsize = [self.FrameDisplayChoice.winfo_width()/100, self.FrameDisplayChoice.winfo_height()/100])
            ax = fig.add_subplot(111)
            ax.boxplot(result)
            ax.grid(True)
            ax.axhline(0, c="r")
            fig.subplots_adjust(top=0.90, bottom = 0.15, left=0.1, right = 0.98)
            ax.set_xticklabels(self.optionsVarChoice[1:], fontsize=8)
            ax.tick_params(axis='y', which='major', labelsize=8)
            ax.set_title("Model parameters", fontsize=10, fontweight='bold')
            ax.set_xlabel("Variables", fontsize=8)
            canvas = Canvas(self.FrameDisplayChoice)
            canvas.pack(fill=BOTH, expand=1)
            figureChoice = FigureCanvasTkAgg(fig, canvas)
            figureChoice.get_tk_widget().pack(fill=BOTH, expand=1)
            #tool = NavigationToolbar2Tk(canvas, self.Frame48H)
            #tool.update()
            figureChoice._tkcanvas.pack(fill=BOTH, expand=1)
            #figureChoice.draw()
            self.addClickable(fig, 3.1)
            self.root.update()
        elif result.shape[1] > 1:
            result = pd.DataFrame(result)
            fig = plt.figure(figsize = [self.FrameDisplayChoice.winfo_width()/100, self.FrameDisplayChoice.winfo_height()/100])
            ax = fig.add_subplot(111)
            mat = ax.imshow(result,aspect='auto')
            if self.varVarChoice.get() != "All":
                ax.set_xlabel("Days", fontsize=8)
                ax.set_xticks(range(0,7))
                ax.set_xticklabels(range(0,7))
                ax.set_ylabel("Hours", fontsize=8)
                ax.set_yticks(range(0,len(self.optionsHourChoice[1:])))
                ax.set_yticklabels(self.optionsHourChoice[1:])
            elif self.varHourChoice.get() != "All":
                ax.set_xlabel("Days", fontsize=8)
                ax.set_xticks(range(0,7))
                ax.set_xticklabels(range(0,7))
                ax.set_ylabel("Variables", fontsize=8)
                ax.set_yticks(range(0,len(self.optionsVarChoice[1:])))
                ax.set_yticklabels(self.optionsVarChoice[1:])
            elif self.varDayChoice.get() != "All":
                ax.set_xlabel("Hours", fontsize=8)
                ax.set_xticks(range(0,24))
                ax.set_xticklabels(range(0,24))
                ax.set_ylabel("Variables", fontsize=8)
                ax.set_yticks(range(0,len(self.optionsVarChoice[1:])))
                ax.set_yticklabels(self.optionsVarChoice[1:])
            ax.tick_params(axis='both', which='major', labelsize=8)
            ax.set_title("Model parameters")
            fig.colorbar(mat)
            fig.tight_layout()
            canvas = Canvas(self.FrameDisplayChoice)
            canvas.pack(fill=BOTH, expand=1)
            figureChoice = FigureCanvasTkAgg(fig, canvas)
            figureChoice.get_tk_widget().pack(fill=BOTH, expand=1)
            #tool = NavigationToolbar2Tk(canvas, self.Frame48H)
            #tool.update()
            figureChoice._tkcanvas.pack(fill=BOTH, expand=1)
            self.addClickable(fig, 3.2)
            self.root.update()
        elif result.shape[1] == 1:
            InsideFrame = Frame(self.FrameDisplayChoice)
            InsideFrame.pack(fill=BOTH, expand=1)
            result = pd.DataFrame(result)
            result.rename(columns={result.columns[0]: "Coeffs"}, inplace=True)
            if self.varHourChoice.get() == "All":
                result["Hours"] = self.optionsHourChoice[1:]
            elif self.varDayChoice.get() == "All":
                result["Days"] = list(range(0,7))
            elif self.varVarChoice.get() != "All":
                result["Vars"] = self.varVarChoice.get()
            else:
                result["Vars"] = self.optionsVarChoice[1:]
            t = Table(InsideFrame, dataframe = result[result.columns[::-1]])
            t.show()
            #config.apply_options({"font":"Garuda"}, t)
            t.redraw()
            
            self.root.update()
        self.root.update()
    
    def drawTS(self, force=True):
        import pandas as pd
        import matplotlib.ticker as ticker
        
        if self.firstTime:
            return
        var1 = self.varTS1.get()
        var2 = self.varTS2.get()
        pathToUse = self.pathDir+"/Runtime/data.csv"
        dataset = pd.read_csv(pathToUse, index_col=0)
        self.axTS.clear()
        self.axTSTwin.clear()
        stopIndex = dataset.index[dataset['day'] == str(self.now)][0]
        if var1 != "None":
            self.axTS.plot(dataset["day"].iloc[0:stopIndex], dataset[var1].iloc[0:stopIndex], label=var1)
            self.axTS.set_ylabel(var1, fontsize=8)
        if var2 != "None":
            self.axTSTwin.plot(dataset["day"].iloc[0:stopIndex], dataset[var2].iloc[0:stopIndex], c="orange", label=var2)
            self.axTSTwin.set_ylabel(var2, fontsize=8)
        self.axTS.xaxis.set_major_locator(ticker.AutoLocator())
        self.axTS.tick_params(axis='y', which='major', labelsize=8)
        self.axTSTwin.tick_params(axis='y', which='major', labelsize=8)
        self.axTS.grid(True)
        plt.setp(self.axTS.xaxis.get_majorticklabels(),
         'rotation', 30, 'ha', "right", 'fontsize', 6)
        self.figTS.subplots_adjust(top=0.90, bottom = 0.23)
        self.axTS.set_title("Training set analysis", fontsize=10, fontweight='bold')
        self.FigureCanvasTS._tkcanvas.pack(fill=BOTH, expand=1)
        lines = []
        labLines = []
        for line in self.axTS.lines:
            lines.append(line)
            labLines.append(line.get_label())
        for line in self.axTSTwin.lines:
            lines.append(line)
            labLines.append(line.get_label())
        self.axTS.legend(lines, labLines)
        if force:
            self.FigureCanvasTS.draw()
        self.root.update()
    
    def updateTS(self):
        import pandas as pd
        import matplotlib.ticker as ticker
        
        pathToUse = self.pathDir+"/Runtime/data.csv"
        dataset = pd.read_csv(pathToUse, index_col=0)
        var1 = self.varTS1.get()
        var2 = self.varTS2.get()
        lineVar1 = self.axTS.get_lines()[0]
        lineVar2 = self.axTSTwin.get_lines()[0]
        newIndex = dataset.index[dataset['day'] == str(self.now)][0]
        if var1 != "None":
            dataVar1X = list(lineVar1.get_xdata())
            dataVar1Y = list(lineVar1.get_ydata())
            dataVar1X.append(dataset['day'].iloc[newIndex])
            #dataVar1X = dataVar1X[1:]
            dataVar1Y.append(dataset[var1].iloc[newIndex])
            #dataVar1Y = dataVar1Y[1:]
            self.axTS.clear()
            self.axTS.plot(dataVar1X, dataVar1Y, label=var1)
            self.axTS.set_ylabel(var1, fontsize=8)
        if var2 != "None":
            dataVar2X = list(lineVar2.get_xdata())
            dataVar2Y = list(lineVar2.get_ydata())
            dataVar2X.append(dataset['day'].iloc[newIndex])
            #dataVar2X = dataVar2X[1:]
            dataVar2Y.append(dataset[var2].iloc[newIndex])
            #dataVar2Y = dataVar2Y[1:]
            self.axTSTwin.clear()
            self.axTSTwin.plot(dataVar2X, dataVar2Y, c="orange", label=var2)
            self.axTSTwin.set_ylabel(var2, fontsize=8)
        self.axTS.xaxis.set_major_locator(ticker.AutoLocator())
        self.axTS.tick_params(axis='y', which='major', labelsize=8)
        self.axTSTwin.tick_params(axis='y', which='major', labelsize=8)
        self.axTS.grid(True)
        plt.setp(self.axTS.xaxis.get_majorticklabels(),
         'rotation', 30, 'ha', "right", 'fontsize', 6)
        self.figTS.subplots_adjust(top=0.90, bottom = 0.23)
        self.axTS.set_title("Training set analysis", fontsize=10, fontweight='bold')
        lines = []
        labLines = []
        for line in self.axTS.lines:
            lines.append(line)
            labLines.append(line.get_label())
        for line in self.axTSTwin.lines:
            lines.append(line)
            labLines.append(line.get_label())
        self.axTS.legend(lines, labLines)
        #self.FigureCanvasTS._tkcanvas.pack(fill=BOTH, expand=1)
        #self.FigureCanvasTS.draw()
        #self.root.update()
    
    def showLegend(self):
        newWindow = tk.Toplevel(self.root)
        img = tk.PhotoImage(file=self.pathDir+'/Imgs/XM.png')
        newWindow.tk.call('wm', 'iconphoto', newWindow._w, img)
        Frame1 = Frame(newWindow)
        Frame1.pack(fill=BOTH, expand=1)
        text2 = tk.Text(Frame1)
        text2.pack(fill=BOTH, expand=1)
        scroll = tk.Scrollbar(Frame1, command=text2.yview)
        scroll.pack(side=RIGHT, fill=Y, expand=1)
        text2.pack(side=LEFT, fill=Y, expand=1)
        text2.configure(yscrollcommand=scroll.set)
        fileLegend = open(self.pathDir+"/Data/legend.txt","r")
        text2.insert(tk.END, fileLegend.read())
        
    def updateGUI(self):
        if self.start == 1:
            global current_date
            self.now = current_date#self.now + timedelta(hours=1)
            self.countDays += 1
            if self.countDays == 24:
                self.countDays = 0
                self.drawChoice()
            self.draw48H()
            self.changeSele48H(False)
            if self.firstTime:
                self.firstTime = False
                self.drawLastEpoch()
                self.drawChoice()
                self.drawTS(False)
            else:
                self.updateLastEpoch()
                self.updateTS()
            self.LabelDate.configure(text="Current time: "+str(self.now))
            print("GUI updated\n")
        #self.root.after(3000, self.updateGUI)
        
    def addClickable(self, figure, frame):
        def on_click(event):
            import io
            import pickle, math
            import matplotlib.ticker as ticker
            from matplotlib.ticker import FormatStrFormatter

            if not event.inaxes: return
            newWindow = tk.Toplevel(self.root)
            Frame1 = Frame(newWindow)
            Frame1.pack(fill=BOTH, expand=1)
            Canvas1 = Canvas(Frame1)
            Canvas1.pack(side=BOTTOM, fill=BOTH, expand=1)
            """
            buf = io.BytesIO()
            pickle.dump(figure, buf)
            buf.seek(0)
            fig2 = pickle.load(buf)
            """
            fig2 = plt.figure()
            ax2 = fig2.add_subplot(111)
            if frame == 1:
                dataX0 = self.ax48H.lines[0].get_xdata()
                dataY0 = self.ax48H.lines[0].get_ydata()
                dataX1 = self.ax48H.lines[1].get_xdata()
                dataY1 = self.ax48H.lines[1].get_ydata()
                twin = True
                try:
                    dataTwin = self.ax48HTwin.lines[0].get_ydata()
                except:
                    twin = False
                ax2.plot(dataX0, dataY0, label="True")
                ax2.plot(dataX1, dataY1, c='orange', label="False")
                if twin:
                    twinAx2 = ax2.twinx()
                    twinAx2.plot(dataX0, dataTwin, c="red", label=self.var48H.get())
                    twinAx2.set_ylabel(self.var48H.get(), fontsize=8)
                    twinAx2.tick_params(axis='y', which='major', labelsize=8)
                lines = []
                labLines = []
                for line in ax2.get_lines():
                    lines.append(line)
                    labLines.append(line.get_label())
                if twin:
                    lines.append(twinAx2.get_lines()[0])
                    labLines.append(twinAx2.get_lines()[0].get_label())
                ax2.xaxis.set_major_locator(ticker.AutoLocator())
                plt.setp(ax2.xaxis.get_majorticklabels(), 'rotation', 30, 'ha', "right", 'fontsize', 6)
                ax2.set_ylabel("Heating load [MWh]", fontsize=8)
                ax2.text(0.45, 0.85, "RMSE = {0:.2f}".format(math.sqrt(mean_squared_error(dataY0, dataY1))), transform=fig2.transFigure);
                fig2.subplots_adjust(top=0.90, bottom = 0.23, left=0.1, right = 0.90)
                ax2.grid(True)
                ax2.legend(lines, labLines)
            elif frame == 2:
                scatter = True
                try:
                    dataX0 = self.axLastEpoch.lines[0].get_xdata()
                    dataY0 = self.axLastEpoch.lines[0].get_ydata()
                    dataTwin = self.axLastEpochTwin.lines[0].get_ydata()
                    scatter = False
                except:
                    dataX0 = self.scatter1.get_offsets()[0][0]
                    dataY0 = self.scatter1.get_offsets()[0][1]
                    dataTwin = self.scatter2.get_offsets()[0][1]
                twinAx2 = ax2.twinx()
                if scatter:
                    ax2.scatter(dataX0, dataY0, label="RMSE")
                    twinAx2.scatter(dataX0, dataTwin, c='orange', label="R^2")
                else:
                    ax2.plot(dataX0, dataY0, label="RMSE")
                    twinAx2.plot(dataX0, dataTwin, c='orange', label="R^2")
                ax2.set_ylabel("Root Mean Squared Error [MWh]", fontsize = 8)
                twinAx2.set_ylabel("R^2", fontsize=8)
                ax2.xaxis.set_major_locator(ticker.AutoLocator())
                ax2.grid(True)
                plt.setp(ax2.xaxis.get_majorticklabels(),
                 'rotation', 30, 'ha', "right", 'fontsize', 6)
                fig2.subplots_adjust(top=0.90, bottom = 0.23, left=0.12, right = 0.88)
                ax2.tick_params(axis='y', which='major', labelsize=8)
                twinAx2.tick_params(axis='y', which='major', labelsize=8)
                twinAx2.yaxis.set_major_formatter(FormatStrFormatter('%.4f'))
                lines = []
                labLines = []
                if not scatter:
                    for line in ax2.get_lines():
                        lines.append(line)
                        labLines.append(line.get_label())
                    lines.append(twinAx2.get_lines()[0])
                    labLines.append(twinAx2.get_lines()[0].get_label())
                    ax2.legend(lines, labLines)
            elif frame == 3.1:
                result = self.getChoice()
                ax2.boxplot(result)
                ax2.grid(True)
                ax2.axhline(0, c="r")
                fig2.subplots_adjust(top=0.90, bottom = 0.15, left=0.1, right = 0.98)
                ax2.set_xticklabels(self.optionsVarChoice[1:], fontsize=8)
                ax2.tick_params(axis='y', which='major', labelsize=8)
                ax2.set_xlabel("Variables", fontsize=8)
            elif frame == 3.2:
                result = self.getChoice()
                mat = ax2.imshow(result,aspect='auto')
                if self.varVarChoice.get() != "All":
                    ax2.set_xlabel("Days", fontsize=8)
                    ax2.set_xticks(range(0,7))
                    ax2.set_xticklabels(range(0,7))
                    ax2.set_ylabel("Hours", fontsize=8)
                    ax2.set_yticks(range(0,len(self.optionsHourChoice[1:])))
                    ax2.set_yticklabels(self.optionsHourChoice[1:])
                elif self.varHourChoice.get() != "All":
                    ax2.set_xlabel("Days", fontsize=8)
                    ax2.set_xticks(range(0,7))
                    ax2.set_xticklabels(range(0,7))
                    ax2.set_ylabel("Variables", fontsize=8)
                    ax2.set_yticks(range(0,len(self.optionsVarChoice[1:])))
                    ax2.set_yticklabels(self.optionsVarChoice[1:])
                elif self.varDayChoice.get() != "All":
                    ax2.set_xlabel("Hours", fontsize=8)
                    ax2.set_xticks(range(0,24))
                    ax2.set_xticklabels(range(0,24))
                    ax2.set_ylabel("Variables", fontsize=8)
                    ax2.set_yticks(range(0,len(self.optionsVarChoice[1:])))
                    ax2.set_yticklabels(self.optionsVarChoice[1:])
                ax2.tick_params(axis='both', which='major', labelsize=8)
                fig2.colorbar(mat)
            elif frame == 4:
                lines = []
                labLines = []
                for line in self.axTS.lines:
                    ax2.plot(line.get_xdata(), line.get_ydata(), label=line.get_label())
                    lines.append(line)
                    labLines.append(line.get_label())
                    ax2.set_ylabel(line.get_label(), fontsize=8)
                twinAx2 = ax2.twinx()
                for line in self.axTSTwin.lines:
                    twinAx2.plot(line.get_xdata(), line.get_ydata(), c="orange", label=line.get_label())
                    lines.append(line)
                    labLines.append(line.get_label())
                    twinAx2.set_ylabel(line.get_label(), fontsize=8)
                ax2.xaxis.set_major_locator(ticker.AutoLocator())
                ax2.tick_params(axis='y', which='major', labelsize=8)
                twinAx2.tick_params(axis='y', which='major', labelsize=8)
                ax2.grid(True)
                plt.setp(ax2.xaxis.get_majorticklabels(),
                 'rotation', 30, 'ha', "right", 'fontsize', 6)
                fig2.subplots_adjust(top=0.90, bottom = 0.23)
                ax2.legend(lines, labLines)
                
            ax2.set_title(str(figure.axes[0].get_title())+", "+str(self.now))
            FigureCanvas1 = FigureCanvasTkAgg(fig2, Canvas1)
            FigureCanvas1._tkcanvas.pack(fill=BOTH, expand=1)
            tool = NavigationToolbar2Tk(FigureCanvas1, Frame1)
            tool.update()
            self.root.update()
            
        figure.canvas.mpl_connect('button_press_event', on_click)
    
    def duplicateFig(self, figure):
        print("Clicked on "+str(figure))


class ParametersWindow:
    def __init__(self, master=None, top=None, pathDir=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85'
        _ana2color = '#ececec' # Closest X11 color: 'gray92'

        self.master = master
        self.root = top
        top.geometry("600x381+407+129")
        top.minsize(1, 1)
        #top.maxsize(1351, 738)
        top.resizable(1, 1)
        top.title("Parameters settings")

        self.FrameTop = tk.Frame(top)
        self.FrameTop.place(relx=0.017, rely=0.021, relheight=0.958
                , relwidth=0.975)
        self.FrameTop.configure(relief='groove')
        self.FrameTop.configure(borderwidth="2")
        self.FrameTop.configure(relief="groove")

        self.FrameHorizon = tk.Frame(self.FrameTop)
        self.FrameHorizon.place(relx=0.051, rely=0.038, relheight=0.151
                , relwidth=0.897)
        self.FrameHorizon.configure(relief='flat')
        self.FrameHorizon.configure(borderwidth="2")

        self.varRadio = tk.IntVar(self.FrameHorizon)
        self.Radio24 = tk.Radiobutton(self.FrameHorizon)
        self.Radio24.place(relx=0.41, rely=0.364, relheight=0.309
                , relwidth=0.112)
        self.Radio24.configure(justify='left')
        self.Radio24.configure(text='''24H''')
        self.Radio24.configure(variable=self.varRadio, value=1)

        self.Radio48 = tk.Radiobutton(self.FrameHorizon)
        self.Radio48.place(relx=0.648, rely=0.364, relheight=0.309
                , relwidth=0.112)
        self.Radio48.configure(justify='left')
        self.Radio48.configure(text='''48H''')
        self.Radio48.configure(variable=self.varRadio, value=2)

        self.LabelHorizon = tk.Label(self.FrameHorizon)
        self.LabelHorizon.place(relx=0.048, rely=0.364, height=15, width=139)
        self.LabelHorizon.configure(text='''Predictive Horizon:''')

        self.FrameRefresh = tk.Frame(self.FrameTop)
        self.FrameRefresh.place(relx=0.051, rely=0.274, relheight=0.205
                , relwidth=0.915)
        self.FrameRefresh.configure(relief='flat')
        self.FrameRefresh.configure(borderwidth="2")

        self.SliderInterval = tk.Scale(self.FrameRefresh, from_=15, to=3600)
        self.SliderInterval.place(relx=0.047, rely=0.4, relwidth=0.893
                , relheight=0.0, height=36, bordermode='ignore')
        self.SliderInterval.configure(length="478")
        self.SliderInterval.configure(orient="horizontal")
        self.SliderInterval.configure(troughcolor="#d9d9d9")

        self.LabelSliderInterval = tk.Label(self.FrameRefresh)
        self.LabelSliderInterval.place(relx=0.047, rely=0.133, height=15
                , width=172)
        self.LabelSliderInterval.configure(text='''Choose the refresh rate:''')

        self.MinusInterval = tk.Button(self.FrameRefresh)
        self.MinusInterval.place(relx=0.007, rely=0.56, height=25, width=20)
        self.MinusInterval.configure(text='''-''', command = lambda: self.upDownInterval("-"))

        self.PlusInterval = tk.Button(self.FrameRefresh)
        self.PlusInterval.place(relx=0.946, rely=0.56, height=25, width=20)
        self.PlusInterval.configure(text='''+''', command = lambda: self.upDownInterval("+"))

        self.FrameDate = tk.Frame(self.FrameTop)
        self.FrameDate.place(relx=0.051, rely=0.575, relheight=0.205
                , relwidth=0.915)
        self.FrameDate.configure(relief='flat')
        self.FrameDate.configure(borderwidth="2")

        self.optionsDate = pd.read_csv(pathDir+"/Data/data.csv")["day"]
        for i in range(len(self.optionsDate)):
            self.optionsDate[i] = self.optionsDate[i].split(" ")[0]
        self.optionsDate = pd.DataFrame(np.unique(self.optionsDate)) 
        self.optionsDate = pd.Series(self.optionsDate.iloc[np.where(self.optionsDate[0] > "2016-02-29")][0])
        self.optionsDate.index = range(self.optionsDate.shape[0])
        
        self.SliderDate = tk.Scale(self.FrameDate, from_ = 0, to = len(self.optionsDate)-1, showvalue=False, label = self.optionsDate[0], command = self.scaleLabels)
        self.SliderDate.place(relx=0.047, rely=0.347, relwidth=0.893, relheight=0.0
                , height=36, bordermode='ignore')
        self.SliderDate.configure(length="478")
        self.SliderDate.configure(orient="horizontal")
        self.SliderDate.configure(troughcolor="#d9d9d9")

        self.LabelDate = tk.Label(self.FrameDate)
        self.LabelDate.place(relx=0.047, rely=0.133, height=15, width=189)
        self.LabelDate.configure(text='''Choose the starting date:''')

        self.MinusDate = tk.Button(self.FrameDate)
        self.MinusDate.place(relx=0.007, rely=0.507, height=25, width=20)
        self.MinusDate.configure(text='''-''', command = lambda: self.upDownDate("-"))

        self.PlusDate = tk.Button(self.FrameDate)
        self.PlusDate.place(relx=0.948, rely=0.467, height=25, width=25)
        self.PlusDate.configure(text='''+''', command = lambda: self.upDownDate("+"))

        self.Confirm = tk.Button(self.FrameTop)
        self.Confirm.place(relx=0.677, rely=0.904, height=25, width=77)
        self.Confirm.configure(text='''Confirm''', command = self.confirm)

        self.Cancel = tk.Button(self.FrameTop)
        self.Cancel.place(relx=0.843, rely=0.904, height=25, width=70)
        self.Cancel.configure(text='''Cancel''', command = self.cancel)
        
        
    def upDownInterval(self, action):
        value = self.SliderInterval.get()
        if value < 3600 and action == "+":
            self.SliderInterval.set(value+1)
        elif value > 15 and action == "-":
            self.SliderInterval.set(value-1)
            
    def upDownDate(self, action):
        value = self.SliderDate.get()
        if value < len(self.optionsDate)-1 and action == "+":
            self.SliderDate.set(value+1)
            self.SliderDate.config(label=self.optionsDate[value+1])
        elif value > 0 and action == "-":
            self.SliderDate.set(value-1)
            self.SliderDate.config(label=self.optionsDate[value-1])
    
    def scaleLabels(self, value):
        self.SliderDate.config(label=self.optionsDate[int(value)])
        
    def confirm(self):
        radio = self.varRadio.get()
        if radio != 1 and radio != 2:
            messagebox.showwarning("Warning!", "Choose one horizon", parent=self.root)
            return
        
        print("Initializing tool...")
        ls = Splash(self.root, "Imgs/hg.gif")
        ls.__enter__()
        if radio == 1:
            set_horizon(24)
        else:
            set_horizon(48)
        set_date(str(self.optionsDate[int(self.SliderDate.get())])+" 00:00:00")
        set_refreshRate(int(self.SliderInterval.get()))
        global startOn
        startOn = True
        forecast_module()
        startOn = False
        ls.__exit__(None,None,None)
        self.root.destroy()
        switchon()
        
    
    def cancel(self):
        self.master.start = 0
        self.master.ButtonStart.configure(text="Start")
        self.root.destroy()
    
############################################################################### 
################################ EXTRA ######################################## 

# Start function    
def switchon():
    global startOn
    global scheduler

    
    if(startOn == False):
        startOn = True
        print('\nStarted\n')                
        scheduler.start()
    
# Pause function    
def switchoff():
    global switch
    global startOn
    global scheduler

    
    if(switch == True and startOn == True):
        switch = False
        print('\nPaused\n')        
        scheduler.pause_job('forecaster')


# Restart function
def restart():
    global switch 
    global scheduler

    if(switch == False and startOn == True):
        switch = True
        print('\nRestarted\n')
        scheduler.resume_job('forecaster')

            
# Exit function        
def kill():
    global scheduler

    scheduler.remove_job('forecaster')
    root.destroy()
    

# GUI definition    
def base():
    root = tk.Tk()
    root.title('Forecaster v.1')
    root.geometry('300x150')
    root.resizable(0, 0)
    
    return root


# Buttons definition
def buttons():    
    global root
    
    frame_button = tk.Frame(root, relief='raised', borderwidth=1)  
    onbutton = tk.Button(frame_button, text = "Start", command = switchon)
    #onbutton = tk.Button(frame_button, text = "Start", command = fast_execution)   
    onbutton.pack(side='left', anchor='w', fill='x', expand='yes', padx=5, pady=5)
    offbutton =  tk.Button(frame_button, text = "Stop", command = switchoff)  
    offbutton.pack(side='left', padx=5, pady=5)
    restartbutton = tk.Button(frame_button, text = "Restart", command = restart)  
    restartbutton.pack(side='left', padx=5, pady=5) 
    killbutton = tk.Button(frame_button, text = "Exit", command = kill)  
    killbutton.pack(side='left', padx=5, pady=5)    
        
    frame_button.pack(fill='x', side='bottom', expand=True)
    
       
# GUI definition    
def GUI():
    global root
    buttons()
    

# Fast predictions
def fast_execution():    
    while True:
        forecast_module()
        
        
        
############################################################################### 
################################ MAIN ######################################### 
        
if __name__ == '__main__':
    #pathDir = '/home/federico_bianchi/Scrivania/Ghothem_v1/Forecaster'
    #pathDir = "/home/francesco/AGSM/XM_HeatForecast_v2+Doc+Readme_for_github/XM_HeatForecast"
    #print(os.path.dirname(os.path.abspath(__file__)))
    
    utils()
    
    #horizon = forecasting_horizon('Enter Forecasting horizon (24h or 48h):')
    #weather_files()
    
    #set_refreshRate(15)
    #set_horizon(48)
    #set_date('2018-01-08 00:00:00')

    global startOn
    startOn = False

    """
    root = base()
    GUI()
    root.mainloop()
    """
    vp_start_gui(os.path.dirname(os.path.abspath(__file__)))





