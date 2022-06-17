#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Provides ways to work with large multidimensional arrays
import numpy as np 
# Allows for further data manipulation and analysis
import pandas as pd 
import matplotlib.pyplot as plt # Plotting
import matplotlib.dates as mdates # Styling dates
get_ipython().run_line_magic('matplotlib', 'inline')

# pip install numpy
# conda install -c anaconda pandas
# conda install -c conda-forge matplotlib

import datetime as dt # For defining dates

import time

# In Powershell Prompt : conda install -c conda-forge multitasking
# pip install -i https://pypi.anaconda.org/ranaroussi/simple yfinance

get_ipython().system('pip3 install yfinance')

import yfinance as yf

# To show all your output File -> Preferences -> Settings Search for Notebook
# Notebook Output Text Line Limit and set to 100

# Used for file handling like deleting files
import os

get_ipython().system('pip install cufflinks')
# conda install -c conda-forge cufflinks-py
# conda install -c plotly plotly
import cufflinks as cf
import plotly.express as px
import plotly.graph_objects as go

# Make Plotly work in your Jupyter Notebook
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
init_notebook_mode(connected=True)
# Use Plotly locally
cf.go_offline()

from plotly.subplots import make_subplots

# New Imports
# Used to get data from a directory
import os
from os import listdir
from os.path import isfile, join

import warnings
warnings.simplefilter("ignore")


# constant

# In[2]:


PATH = "D:/Python for Finance/ichimoku/"

# Start end date defaults
S_DATE = "2021-02-01"
E_DATE = "2022-12-06"
S_DATE_DT = pd.to_datetime(S_DATE)
E_DATE_DT = pd.to_datetime(E_DATE)


# Get Column Data from CSV

# In[3]:


def get_column_from_csv(file, col_name):
    # Try to get the file and if it doesn't exist issue a warning
    try:
        df = pd.read_csv(file)
    except FileNotFoundError:
        print("File Doesn't Exist")
    else:
        return df[col_name]


# Get Stock Tickers

# In[4]:


tickers = get_column_from_csv("D:/Python for Finance/Bombay.csv", "Ticker")
print(len(tickers))


# Save Stock Data to CSV

# In[5]:


# Function that gets a dataframe by providing a ticker and starting date
def save_to_csv_from_yahoo(folder, ticker):
    stock = yf.Ticker(ticker)
    
    try:
        print("Get Data for : ", ticker)
        # Get historical closing price data
        df = stock.history(period="1y")
    
        # Wait 2 seconds
        #time.sleep(2)
        
        # Remove the period for saving the file name
        # Save data to a CSV file
        # File to save to 
        the_file = folder + ticker.replace(".", "_") + '.csv'
        print(the_file, " Saved")
        df.to_csv(the_file)
    except Exception as ex:
        print("Couldn't Get Data for :", ticker)


# Download All Stocks

# In[ ]:


for x in range(0, 4105):
    save_to_csv_from_yahoo(PATH, tickers[x])
    print("Finished")


# Get Dataframe from CSV

# In[7]:


# Reads a dataframe from the CSV file, changes index to date and returns it
def get_stock_df_from_csv(ticker):
    
    # Try to get the file and if it doesn't exist issue a warning
    try:
        df = pd.read_csv(PATH + ticker + '.csv')
#        df = pd.read_csv(PATH + ticker + '.csv', index_col=0)
    except FileNotFoundError:
        print("File Doesn't Exist")
    else:
        return df


# In[8]:


files = [x for x in listdir(PATH) if isfile(join(PATH, x))]
tickers = [os.path.splitext(x)[0] for x in files]
tickers
# tickers.remove('.ds_Store') MacOS Only
tickers.sort()
len(tickers)


# In[9]:


def add_Ichimoku(df):
    # Conversion
    hi_val = df['High'].rolling(window=9).max()
    low_val = df['Low'].rolling(window=9).min()
    df['Conversion'] = (hi_val + low_val) / 2

    # Baseline
    hi_val2 = df['High'].rolling(window=26).max()
    low_val2 = df['Low'].rolling(window=26).min()
    df['Baseline'] = (hi_val2 + low_val2) / 2

    # Spans
    df['SpanA'] = ((df['Conversion'] + df['Baseline']) / 2).shift(26)
    hi_val3 = df['High'].rolling(window=52).max()
    low_val3 = df['Low'].rolling(window=52).min()
    df['SpanB'] = ((hi_val3 + low_val3) / 2).shift(26)
    df['Lagging'] = df['Close'].shift(-26)

    return df


# In[10]:


list1 = []
for i in range(26):
    list1.append(i)


# In[11]:


for x in tickers:
    try:
        print("Working on :", x)
        new_df = get_stock_df_from_csv(x)
        new_df = new_df.append(list1, ignore_index=True)
        new_df = add_Ichimoku(new_df)
        new_df.to_csv(PATH + x + '.csv')
    except Exception as ex:
        print(ex)


# In[12]:


new_df = get_stock_df_from_csv('1STCUS_BO')
print (new_df['SpanA'].iloc[-1])
print (new_df['SpanB'].iloc[-1])
print (new_df['Conversion'].iloc[-27])
print (new_df['Baseline'].iloc[-27])
print (new_df['Lagging'].iloc[-53])
print (new_df['Close'].iloc[-27])
print (new_df['SpanA'].iloc[-27])
print (new_df['Close'].iloc[-1])
print (new_df['SpanA'].iloc[-28])
print (new_df['Close'].iloc[-28])


# In[13]:


list2 = []
for x in tickers:
    try:
        #print("Working on :", x)
        new_df = get_stock_df_from_csv(x)
        if new_df['SpanA'].iloc[-1] > new_df['SpanB'].iloc[-1]:
            
            if new_df['Conversion'].iloc[-27] > new_df['Baseline'].iloc[-27]:
                print ('1')
                if new_df['Lagging'].iloc[-53] > new_df['Close'].iloc[-53]:
                    print ('2')
                    if new_df['SpanA'].iloc[-27] <= new_df['Close'].iloc[-27]:
                        print ('3')
                        if new_df['SpanA'].iloc[-28] >= new_df['Close'].iloc[-28] or new_df['SpanA'].iloc[-29] >= new_df['Close'].iloc[-29]:
                            print (x)
                            list2.append(x)                    
    except Exception as ex:
       print(ex)


# In[14]:


list2


# In[ ]:




