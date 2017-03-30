#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 09:52:13 2017

@author: fhellander
"""

import datetime as dt
from pytrends.request import TrendReq
import pandas as pd
from pandas_datareader import data as web
import seaborn as sns
import matplotlib.pyplot as plt

csv_filepath = 'C-rad.csv'


google_trends=pd.read_csv(csv_filepath,  index_col=0)
google_trends.index = [dt.datetime.strptime(index, '%Y-%m-%d') for index in google_trends.index]
google_trends.index = [dt.date(t.year,t.month,t.day) for t in google_trends.index]

window_size=250
win_start=google_trends.index[0]
win_end=win_start +dt.timedelta(days=window_size)

#Creating array for storing sampling
index=pd.date_range(startdate, enddate)
index =[dt.date(t.year,t.month,t.day) for t in index]
sampled=pd.DataFrame( data=0.0 , index=index, columns=['Google Trend', 'Samplings'])


