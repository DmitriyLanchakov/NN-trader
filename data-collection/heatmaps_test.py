#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 20 10:47:01 2017

@author: fhellander
"""


import datetime as dt
from pytrends.request import TrendReq
import pandas as pd
from pandas_datareader import data as web
import seaborn as sns



enddate=dt.date.today() - dt.timedelta(days=1)
startdate= enddate - dt.timedelta(days=265)
google_username = "delander58@gmail.com"
google_password = "Oddshora1"
keyword=['Hövding']


#Yahoo finance object and pulling data
share='HOVD.ST'
share_df=web.DataReader(share, 'yahoo', startdate, enddate)
share_df.index = [dt.date(t.year,t.month,t.day) for t in share_df.index]



# connect to Google
connector = TrendReq(google_username, google_password)
timeframe=startdate.strftime("%Y-%m-%d") +" " + enddate.strftime("%Y-%m-%d")
connector.build_payload(kw_list=keyword, timeframe=timeframe, geo='SE')
google_trends = connector.interest_over_time()
google_trends.index = [dt.date(t.year,t.month,t.day) for t in google_trends.index]




glt_rm2=pd.rolling_mean(google_trends, 2, min_periods=1) ; glt_rm2=glt_rm2.rename(columns={keyword[0]:'GT rm2'})
glt_rm3=pd.rolling_mean(google_trends, 3, min_periods=1) ; glt_rm3=glt_rm3.rename(columns={keyword[0]:'GT rm3'})
glt_rm5=pd.rolling_mean(google_trends, 5, min_periods=1); glt_rm5=glt_rm5.rename(columns={keyword[0]:'GT rm5'})
glt_rm7=pd.rolling_mean(google_trends, 7, min_periods=1) ; glt_rm7=glt_rm7.rename(columns={keyword[0]:'GT rm7'})
glt_rm10=pd.rolling_mean(google_trends, 10, min_periods=1) ; glt_rm10=glt_rm10.rename(columns={keyword[0]:'GT rm10'})
google_trends=google_trends.rename(columns={keyword[0]:'GT'})

daily_return=share_df['Adj Close'].pct_change(1)*100
daily_return=daily_return.rename('daily return')
return_1day=share_df['Adj Close'].pct_change(1)*100 ; return_1day= return_1day.shift(-1)                  
return_1day=return_1day.rename('in 1day')
return_2days=share_df['Adj Close'].pct_change(2)*100 ; return_2days= return_2days.shift(-2)
return_2days=return_2days.rename('in 2day')
return_3days=share_df['Adj Close'].pct_change(3)*100 ; return_3days= return_3days.shift(-3)
return_3days=return_3days.rename('in 3day')
return_4days=share_df['Adj Close'].pct_change(4)*100 ; return_4days= return_4days.shift(-4)
return_4days=return_4days.rename('in 4day')
return_5days=share_df['Adj Close'].pct_change(5)*100 ; return_5days= return_5days.shift(-5)
return_5days=return_5days.rename('in 5day')
return_10days=share_df['Adj Close'].pct_change(10)*100 ; return_10days= return_10days.shift(-10)
return_10days=return_10days.rename('in 10day')


correlation_list=[google_trends, glt_rm2,glt_rm3,glt_rm5,glt_rm7, glt_rm10, daily_return, return_1day, return_2days, return_3days, return_4days, return_5days, return_10days ]



joined = pd.concat(correlation_list, axis=1)
correlations = joined.corr()
ax = plt.axes()
ax.set_title(keyword)
sns.heatmap(correlations, annot=True, fmt=".2f")




