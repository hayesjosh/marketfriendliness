# "Housing Market Friendliness App"
This is a comparison tool to empower homebuyers to find those housing markets that will likely be a good fit. I created this project while a Doctoral Fellow at The Data Incubator in San Francisco. 


## Overview
This project uses data from Freddie Mac. It is deployed on Heroku, and runs with Flask.

### Step 1: Gather, Clean, and Transform Data
- I sample the 28 Million anonymized home loans available at http://www.freddiemac.com/research/datasets/sf_loanlevel_dataset.html
- This data ranges from 1991 to 2018

### Step 2: Model future competitiveness
- I use time series analyses and an unsupervised machine learning model to account for each region's previous values and make predictions going into 2019. 

### Step 3: Compare users values to predictions
- Take user input (Credit Score and Location), and create interactive visualizations to showcase how competitive that specific user will be across their chosen region. 

### Step 4: Productionalization
- This app is available now. It is hosted on Heroku:
    Visit it at: https://marketfriendliness.herokuapp.com/
