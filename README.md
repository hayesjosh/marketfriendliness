# "Housing Market Friendliness App"
This is a comparison tool to empower home-buyers to find those housing markets that will likely be a good fit. I created this project while a Doctoral Fellow at The Data Incubator, San Francisco.


## Overview
This project uses publicly available data from Freddie Mac. It is deployed on Heroku, and runs with Flask.

### Step 1: Gather, Clean, and Transform Data
- I sample the 26 Million anonymized home loans available at http://www.freddiemac.com/research/datasets/sf_loanlevel_dataset.html
- This data ranges from 1991 to 2018

### Step 2: Model future competitiveness
- I use time series analyses and an ARIMA model to account for each region's previous values and make 6-months of future predictions.

### Step 3: Compare users values to predictions
- Take user input (Credit Score, Location, and Graph Preference), and create interactive visualizations to showcase how competitive that specific user will be across their chosen region.

### Step 4: Productionalization
- This app is available now. It is hosted on Heroku:
    - Visit it at: https://marketfriendliness.herokuapp.com/
