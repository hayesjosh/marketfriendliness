# -*- coding: utf-8 -*-
"""
Created on Sun Sep  2 11:30:49 2018

A Python File to Input all_years of mortgage data from Freddie Mac

@author: Joshua D Hayes
"""

#Importing packages
import numpy as np
import pandas as pd
import os as os
import feather 
import datetime

#Checking current working directory
os.getcwd()
#Setting current working directory
  #On PC
#os.chdir("D:\Dropbox\Work\")
  #On MacAir
os.chdir("/Users/hayes/Dropbox/Work/DI/FinalProject")

#Setting file_list to be all files in data directory

#Importing the sample data set
dmort = feather.read_dataframe("Data/dmort.feather")

#checking it out
dmort.shape
dmort.dtypes
dmort.head(10)
dmort.describe
dmort.count()
dmort.isnull().sum()

##Cleaning
#NaN/Missing
dmort.dropna()
#dmort.fillna()

#Fix zipcodes to be a number-- it has some weird values throwing it off
dmort['zipcode'] = dmort['zipcode'].replace("",None)
dmort['zipcode'] = dmort['zipcode'].astype(int)

#FTHB recode
dmort['flag_fthb'] = dmort['flag_fthb'].replace("9",0)
dmort['flag_fthb'] = dmort['flag_fthb'].replace("Y", 1)
dmort['flag_fthb'] = dmort['flag_fthb'].replace("N",0)
dmort['flag_fthb'].astype(int)
###Recoded!

##TIME
#change date info to be formatted correctly as a datetime object
dmort['loanDate'] = pd.to_datetime(dmort['dt_first_pi'], format= '%Y%m')
#create new columns for year and month
dmort['year'] = dmort['loanDate'].dt.year
dmort['month'] = dmort['loanDate'].dt.month
###Recoded!

##STATE
hm = set(dmort['st'])
len(hm)
#54 instead of 50... not good. we'll have to drop those. 
dmort = dmort[dmort['st'] != 'PR']
dmort = dmort[dmort['st'] != 'DC']
dmort = dmort[dmort['st'] != 'VI']
dmort = dmort[dmort['st'] != 'GU']
#Ahh, there we go. 

#cleaning out the old time var and loan id var
dmort = dmort[dmort.columns.drop('dt_first_pi', 'id_loan')]

dmort.head(10)
#Looks like we're all cleaned up!

#############MAKING NEW VARS
##Making vars
####AvgFico
dmort['fico'].max()
dmort['fico'].min()
dmort['fico'].max() - dmort['fico'].min()
#we got some 9999 values in there for missing. let's just replace them with actual missing. 
dmort['fico'].sum()
dmort['fico'] = dmort['fico'].replace(9999, None)
#creating the new column with average fico by state
dmort['avgFico'] = dmort.groupby(['st'])['fico'].transform('mean')



####%FTHB
#first need to calculate out the count of all home loans by category
dmort['loan_n'] = dmort.groupby(['st'])['flag_fthb'].transform('count')
#then need to do a ratio of FTHB over all loans by category
dmort['FTHB'] = dmort['flag_fthb'].astype(int)
#creating the number of first time home buyers by state
dmort['loan_fthb_n'] = dmort.groupby(['st'])['flag_fthb'].transform('sum')
#creating the percentage of fthb over all loans, multiplying by 100 to be more intuitive
dmort['fthb_perc'] = dmort['loan_fthb_n'] / dmort['loan_n'] * 100    

#looking at it
dmort.head(10)


