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
import random


#--------------INPUTS NEEDED ----------------------------
google_username = "scrapperpapper1@gmail.com"
google_password = "Oddshora1"
keyword=['Lucara Diamond']
enddate=dt.date(2017,3,20)
startdate= dt.date(2013,4,28)
sample_win_size=250
min_sample_size=100
sleeps=2 #delay not to overload google trends request
#--------------INPUTS NEEDED ----------------------------



#Creating  array for storing sampling
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
while (win_back <= enddate) and ((win_front - win_back).days>=min_sample_size):
    
    #Printing status and % progress
    print('Sampling run number: %i' %run)
    print('Sampling %.2f percent complete' %(100.0*run/(sample_win_size+(enddate-startdate).days-min_sample_size )))
    
    
    #Pulling googel trends data to sampling window via googel trends API
    timeframe=win_back.strftime("%Y-%m-%d") +" " + win_front.strftime("%Y-%m-%d")
    connector.build_payload(kw_list=keyword, timeframe=timeframe, geo='SE')
    window = connector.interest_over_time()
    window.index = [dt.date(t.year,t.month,t.day) for t in window.index]
    time.sleep(sleeps*random.random())

    #Adding google trends data to corresponding date in sampling dataframe
    for d in window.index:
        if d in sampled.index:
            sampled.loc[d]['Google Trend']=sampled.loc[d]['Google Trend'] +window.loc[d][keyword]
            sampled.loc[d]['Samplings']=sampled.loc[d]['Samplings'] +1
            
     #Shifting sampling window forward by one day                  
    win_front=win_front+ dt.timedelta(days=1)    
    win_back=win_back + dt.timedelta(days=1)  
    
    #If end date is reached sampling window size shrunk by one day
    if (dt.date.today()-win_front).days<=3:
        win_front = dt.date.today()-dt.timedelta(3)
      
    run+=1
            

#normalizing each date according to the number of samples drawn
sampled['Google Trend'] = sampled['Google Trend']/sampled['Samplings']


#Saving sampled data from googel to CSV file and pickle file
sampled.to_pickle(keyword[0]+'.p')
sampled.to_csv(keyword[0]+'.csv', columns=['Google Trend'], index=True)
      
