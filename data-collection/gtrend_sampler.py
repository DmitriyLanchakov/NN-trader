#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 22:15:18 2017

@author: fhellander
"""

import datetime as dt
from pytrends.request import TrendReq
import pandas as pd
import time
import matplotlib.pyplot as plt
import random


#INPUTS
google_username = "fredrik.hellander@gmail.com"
google_password = "Hellokitt3n"
keyword=['C-rad']
enddate=dt.date.today() - dt.timedelta(days=3)
startdate= enddate - dt.timedelta(days=365*2)
sample_win_size=250
min_sample_size=100
sleeps=30


#Creating array for storing sampling
index=pd.date_range(startdate, enddate)
index =[dt.date(t.year,t.month,t.day) for t in index]
sampled=pd.DataFrame( data=0.0 , index=index, columns=['Google Trend', 'Samplings'])


#Google connect object
connector = TrendReq(google_username, google_password)

#Sampling window starting points
win_front=startdate
win_back=win_front-dt.timedelta(days=(sample_win_size-1))

#sampling while end of sampling window is not infront of enddate and 
#sample window sice has not been shrunk to less than min_sample_size
run=0
while (win_back <= enddate) and ((win_front - win_back).days>=min_sample_size) :
    
    print('Sampling run', run)
    print('% Complete', (100.0*run/(sample_win_size+(enddate-startdate).days-min_sample_size )))
   
    timeframe=win_back.strftime("%Y-%m-%d") +" " + win_front.strftime("%Y-%m-%d")
    connector.build_payload(kw_list=keyword, timeframe=timeframe, geo='SE')
    window = connector.interest_over_time()
    window.index = [dt.date(t.year,t.month,t.day) for t in window.index]
    
    time.sleep(sleeps*random.random())

    for d in window.index:
        if d in sampled.index:
            sampled.loc[d]['Google Trend']=sampled.loc[d]['Google Trend'] +window.loc[d][keyword]
            sampled.loc[d]['Samplings']=sampled.loc[d]['Samplings'] +1
            
    win_front=win_front+ dt.timedelta(days=1)    
    win_back=win_back + dt.timedelta(days=1)  
    
    if (dt.date.today()-win_front).days<=3:
        win_front = dt.date.today()-dt.timedelta(3)
    
    run+=1
            

#normalizing
sampled['Google Trend'] = sampled['Google Trend']/sampled['Samplings']

endcomp=enddate
startcomp= enddate - dt.timedelta(days=250)

connector = TrendReq(google_username, google_password)           
timeframe=startcomp.strftime("%Y-%m-%d") +" " + endcomp.strftime("%Y-%m-%d")
connector.build_payload(kw_list=keyword, timeframe=timeframe, geo='SE')
compare = connector.interest_over_time()          
    

        

ax=plt.axes()
sampled['Google Trend'].plot()
compare['Cortus Energy'].plot()
            
            
        

glt_rm5=pd.rolling_mean(sampled['Google Trend'], 5, min_periods=1)    

ax=plt.axes()
sampled['Google Trend'].plot()
glt_rm5.plot()
