#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 18 13:21:22 2017

@author: fhellander
"""



from pytrends.request import TrendReq
import time
from random import randint
import os
import datetime as dt
import numpy as np
import pandas as pd





google_username = "delander58@gmail.com"
google_password = "Oddshora1"


keyword=['Starbreeze']

# connect to Google
connector = TrendReq(google_username, google_password)


#connector.build_payload(kw_list=keyword, timeframe='2016-04-01 2017-03-01', geo='SE')
#
##pytrends = build_payload(kw_list, cat=0, timeframe='today 5-y', geo='', gprop='')
#
#
#weekly_data = connector.interest_over_time()
#weekly_data.index = [datetime.date(t.year,t.month,t.day) for t in weekly_data.index]
#
#
#
#
#
#
##weekly data starts according to week, finding first and last date
#startdate=weekly_data.index[0]
#enddate=weekly_data.index[-1]
#
##Create datetime index according to weekly data
#dateindex = pd.date_range(start=startdate, end=enddate)
#dateindex= [dt.date(t.year,t.month,t.day) for t in dateindex]
#
#
##Initialize dateframe to store daily google trends score
#rescaled_daily_data = pd.DataFrame(data=0.0, index=dateindex[:-1], columns=keyword)
#
##Initialize values for sliding windown pulling daily trends data
#
#day_win_start=startdate
#day_win_stop=startdate + dt.timedelta(days=60)
#
#
#
##Pulling first daily frame from google trends
#timeframe=day_win_start.strftime("%Y-%m-%d") +" " + day_win_stop.strftime("%Y-%m-%d")
#connector.build_payload(kw_list=keyword, timeframe=timeframe, geo='SE')
#daily_data = connector.interest_over_time()
#daily_data.index = [dt.date(t.year,t.month,t.day) for t in daily_data.index]
#
#
#
##Loooping over all dates in weekly data
#for d in weekly_data.index:
#    
#    if d==weekly_data.index[-1]:
#        break
#    
#    if (d+dt.timedelta(days=7)) >= day_win_stop:
#    
#        day_win_start=d
#        day_win_stop= d+dt.timedelta(days=60)
#        timeframe=day_win_start.strftime("%Y-%m-%d") +" " + day_win_stop.strftime("%Y-%m-%d")
#        connector.build_payload(kw_list=keyword, timeframe=timeframe, geo='SE')
#        daily_data = connector.interest_over_time()
#        daily_data.index = [dt.date(t.year,t.month,t.day) for t in daily_data.index]    
#    
#    
#    #Trapezoidal integration
#    searchvol=0.0
#    for i in range(0,7):
#        int1=daily_data.loc[d+dt.timedelta(days=i)][0]
#        int2=daily_data.loc[d+dt.timedelta(days=(i+1))][0]
#        searchvol=+ 0.5*(int1+int2)
#        
#    scale = weekly_data.loc[d+dt.timedelta(days=7)][0]/100.0
#    scaled_vol=searchvol*scale
#    
#    for i in range(0,7):
#        if searchvol == 0.0:
#            break
#        rescaled_daily_data.loc[d+dt.timedelta(days=i)][0]= daily_data.loc[d+dt.timedelta(days=i)][0]/searchvol *scaled_vol
#        
#                                
#rescaled_daily_data = rescaled_daily_data*100/rescaled_daily_data.max()




connector.build_payload(kw_list=keyword, timeframe='2016-07-01 2017-03-01', geo='SE')   
ref1 = connector.interest_over_time()   

connector.build_payload(kw_list=keyword, timeframe='2016-01-01 2016-08-01', geo='SE')   
ref2 = connector.interest_over_time()   

connector.build_payload(kw_list=keyword, timeframe='2016-06-01 2016-09-01', geo='SE')   
ref3 = connector.interest_over_time()   



ref1.index = [dt.date(t.year,t.month,t.day) for t in ref1.index]
ref2.index = [dt.date(t.year,t.month,t.day) for t in ref2.index]


#Plotting a abit

#ax=rescaled_daily_data.plot()
#
#ref1.plot(ax=ax)
##ref2.plot(ax=ax)
#ref3.plot(ax=ax)
#
#plt.savefig('test.png')



    
    
    
