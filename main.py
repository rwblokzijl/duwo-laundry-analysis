#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import timedelta
from datetime import time as datetime_time
plt.style.use('seaborn-whitegrid')


# In[2]:


# = pd.DataFrame(columns=['date', 'washers', 'dryers'])
#raw_data.read_csv("./both", header=None)

headers = ['datetime', 'wash', 'dry']
dtypes = {'datetime': 'str', 'wash': 'int', 'dry': 'int'}
parse_dates = ['datetime']
raw_data = pd.read_csv("./data", sep=',', header=None, names=headers, dtype=dtypes, parse_dates=parse_dates, date_parser=pd.to_datetime)
#print(raw_data.dtypes)
#print(raw_data)


# In[3]:


def shift_forward(data):
    local_data=data.copy()
    local_data['datetime'] = [time + timedelta(hours=4) for time in local_data['datetime']]
    return local_data

def shift_back(data):
    local_data=data.copy()
    local_data['datetime'] = [time + timedelta(hours=-4) for time in local_data['datetime']]
    return local_data
    
shifted_data = shift_forward(shift_back(raw_data))
#print(shifted_data)


# In[4]:


def get_by_months(data):
    return[g.reset_index() for n, g in data.set_index('datetime').groupby(pd.Grouper(freq='M'))]

months = get_by_months(raw_data)
#print(pd.concat(months[1:3]))


# In[5]:


def get_weekdays(data):
    return data[data.set_index('datetime').index.dayofweek < 5]

def get_weekends(data):
    return data[data.set_index('datetime').index.dayofweek >= 5]

#print(get_weekdays(months[1]))
#print(get_weekends(months[1]))


# In[6]:


def average_range(data):
    local_data=data.copy()
    local_data['datetime'] = [time.floor("5min").time() for time in local_data['datetime']]
    return local_data.set_index('datetime').groupby('datetime').mean().reset_index()

#print(average_range(months[1]))


# In[7]:


def shift_time_forward(data):
    local_data=data.copy()
    local_data['datetime'] = [datetime_time((time.hour + 4)%24, time.minute) for time in local_data['datetime']]
    return local_data

def make_pretty(data_ref):
    data = data_ref.copy()
    data.names = ["Time", "Washers Available", "Dryers Available"]

def plot_data(data_ref, title, filename):
    data = data_ref.copy()
    data['int_index'] = range(len(data))
    ticks=[time.time() for time in pd.date_range(start='1/1/2018 4:00', end='1/3/2018', freq='4H')]
    tickss=[tick.strftime("%H:%M") for tick in ticks]
    ax = data.plot(x="datetime", y=["wash", "dry"], figsize=(12, 6), xticks=ticks, title=title)
    ax.set_xticklabels(tickss)
    ax.legend(["Washers Available", "Dryers Available"])
    ax.set_xlabel("Time")
    fig = ax.get_figure()
    fig.savefig("plots/"+filename)
    plt.close(fig)


#plot_data(average_range(get_weekdays(get_by_months(shift_back(raw_data))[1])), "Weekdays Jan 2019")


# In[8]:


def process_range(data, label, prefix):
    plot_data(average_range(get_weekdays(data)), "Weekdays " + label, prefix + "_weekday_" + label.replace(" ", "_").lower() + ".png")
    plot_data(average_range(get_weekends(data)), "Weekend " + label, prefix + "_weekend_" + label.replace(" ", "_").lower() + ".png")


# In[9]:


months = get_by_months(shift_back(raw_data))[1:]


# In[10]:


for month in months:
    title = month['datetime'][0].strftime("%B %Y")
    m = month['datetime'][0].month
    y = month['datetime'][0].year
    pref = str(y) + "." + str(m).zfill(2)
    process_range(month, title, pref)


# In[11]:


process_range(shift_back(raw_data), "all time Average", "0.0")

