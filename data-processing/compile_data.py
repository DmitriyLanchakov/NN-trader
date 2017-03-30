#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 25 14:46:26 2017

@author: fhellander
"""

import pandas as pd
import datetime as dt
from pandas_datareader import data as web
import numpy as np




stocks= ['Fingerprint Cards', 'Anoto', 'Shamaran', 'Africa Oil', 'Kancera', 
'Cybaero', 'Cassandra Oil', 'Arcam', 'Lucara Diamond', 'Starbreeze', 'Precise Biometrics']




gt_norm_period=60
rolling_mean_periods = [2,5,7,14,21,28]

root='../data-collection/Google_trends/'



ticker_key={
        'Fingerprint Cards':'FING-B.ST',
        'Anoto':'ANOT.ST',
        'Shamaran':'SNM.ST',
        'Africa Oil':'AOI.ST',
        'Kancera':'KAN.ST',
        'Cybaero':'CBA.ST',
        'Cassandra Oil':'CASO.ST',
        'Arcam':'ARCM.ST',
        'Lucara Diamond':'LUC.ST',
        'Starbreeze':'STAR-B.ST',
        'Precise Biometrics':'PREC.ST'}

vol_norm_period = 60

vol_rm_periods = [1,2,5,10,15,20]
gain_lags = [1,2,3,4,5,10]



price_norm_periods = [60]
price_rm_periods = [1,2,5,10,15,20]


reg_target=['5Day_Gain']
GT_variables=['Google Trend', 'RM_2', 'RM_5', 'RM_7', 'RM_14']
vol_variables = ['NormVol_RM_1', 'NormVol_RM_2', 'NormVol_RM_5', 'NormVol_RM_10', 'NormVol_RM_15' ]
price_variables = ['P_RM1_norm60', 'P_RM2_norm60', 'P_RM5_norm60', 'P_RM10_norm60', 'P_RM15_norm60']

input_variables = vol_variables + price_variables


validation_days=100

#Dictionary to save google trends data for each stock
google_trends={}

#Dictonary to save financial data
stock_data = {}

for stock in stocks:   
    
    #Reading CSV file from database
    path=root+stock +'.csv'
    google_trends[stock] = pd.read_csv(path, index_col=0)
    google_trends[stock].index = [dt.datetime.strptime(index, '%Y-%m-%d') for index in google_trends[stock].index]
    google_trends[stock].index = [dt.date(t.year,t.month,t.day) for t in google_trends[stock].index]
    
    #Calulating rolling mean for normalization
    gt_norm=pd.rolling_mean(google_trends[stock], gt_norm_period, min_periods=gt_norm_period) 
    google_trends[stock] = (google_trends[stock]- gt_norm)/gt_norm

    #Calculating all rolling means from the normalized values and saving 
    for period in rolling_mean_periods:
        rolling_mean=pd.rolling_mean( google_trends[stock]['Google Trend'], period, min_periods=period).rename('RM_' + str(period))
        google_trends[stock] = pd.concat([google_trends[stock], rolling_mean], axis=1)


    #Getting ticker symbol and reading yahoo finance data
    ticker=ticker_key[stock]
    stock_data[stock] = web.DataReader(ticker, 'yahoo', google_trends[stock].index[0], google_trends[stock].index[-1])
    stock_data[stock].index = [dt.date(t.year,t.month,t.day) for t in stock_data[stock].index]


    #Calulating rolling volume mean for normalization
    vol_norm=pd.rolling_mean(stock_data[stock]['Volume'], vol_norm_period, min_periods=vol_norm_period) 

    #Calculating volume short rolling means, normalizing and saving 
    for period in vol_rm_periods:
        rolling_mean=pd.rolling_mean(stock_data[stock]['Volume'], period, min_periods=period)
        rolling_mean= ((rolling_mean -vol_norm)/vol_norm).rename('NormVol_RM_' + str(period))
        stock_data[stock] = pd.concat([stock_data[stock], rolling_mean], axis=1)


    #Calculating percentage change from day before
    gain=stock_data[stock]['Adj Close'].pct_change(1).rename('0Day_Gain')*100
    stock_data[stock] = pd.concat([stock_data[stock], gain], axis=1)   
      
    #Calculating return X days into the future     
    for lag in gain_lags:
        gain=stock_data[stock]['Adj Close'].pct_change(lag).shift(-lag).rename(str(lag)+'Day_Gain')*100
        stock_data[stock] = pd.concat([stock_data[stock], gain], axis=1)

    #Calculating rolling averages on adjusted close normalised against different long rolling avg.
    for norm_period in price_norm_periods:
        norm_price = pd.rolling_mean(stock_data[stock]['Adj Close'], norm_period, min_periods=norm_period)
        for rm_period in price_rm_periods:
           rolling_mean=pd.rolling_mean( stock_data[stock]['Adj Close'], rm_period, min_periods=rm_period)
           rolling_mean = ((rolling_mean - norm_price)/norm_price).rename('P_RM' + str(rm_period)+'_norm' + str(norm_period)) 
           stock_data[stock] = pd.concat([stock_data[stock], rolling_mean], axis=1)               



#Initializing dicts and arrays to sort data into training and validation 
reg_values={}
input_data={}
training_data = np.empty((0,len(input_variables + GT_variables)))
training_reg = np.empty((0,1))
validation_data = np.empty((0,len(input_variables + GT_variables)))
validation_reg = np.empty((0,1))


#Selecting input variables to be used and removing any dates with NA data
for stock in stocks: 
    input_data[stock] = stock_data[stock][input_variables +reg_target]
    gt_inputs = google_trends[stock][GT_variables]
    input_data[stock] = pd.concat([input_data[stock], gt_inputs], axis=1).dropna(axis=0) 
    string='Valid data for ' + str(stock) + ' in range ' +input_data[stock].index[0].strftime('%Y-%m-%d') +' to ' +  input_data[stock].index[-1].strftime('%Y-%m-%d')
    print(string)   
    reg_values[stock] = input_data[stock][reg_target]
    del input_data[stock][reg_target[0]]
    
    
    #Splitting training and validation data in chronological order and according to nr validation days
    valid_date_split = stock_data[stock].index[-1] - dt.timedelta(days=validation_days)
    

    #Slicing data and saving np arrays 
    np.save('training_data__' + stock,input_data[stock].loc[:valid_date_split].as_matrix())
    np.save('validation_data_' +stock, input_data[stock].loc[valid_date_split:].as_matrix())
    np.save('training_reg_' + stock,reg_values[stock].loc[:valid_date_split].as_matrix() )
    np.save('validation_reg_' +stock, reg_values[stock].loc[valid_date_split:].as_matrix())
    
    np.save('backtest_data_' +stock, input_data[stock].loc[valid_date_split:].as_matrix())
    np.save('backtest_price_' +stock, stock_data[stock]['Adj Close'].loc[valid_date_split:].as_matrix())


print('Variables used: ' +str(GT_variables) + str(input_variables ))
print('Regression Goal: ' +str(reg_target))





