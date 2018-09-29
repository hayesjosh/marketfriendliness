# My Personal Version of DSI Flask Ticker Tracker on Heroku
I am adding this to my Github as a milestone project requirement for the bootcamp.

# Flask on Heroku

This project ties together some important concepts and
technologies from Git, Flask, JSON, Pandas, Requests, Heroku, and Bokeh.

## Step 1: Get data from API and put it in pandas
- Uses the `requests` library to stock ticker data from a public API. This is in JSON format, and had to be put into a pandas dataframe.
- The project includes some interactivity by having the user submit a form which determines which data is requested.

## Step 2: Use Bokeh to plot pandas data
- Constructs a Bokeh plot from the dataframe.
- Makes the plot visible on a website through embedded HTML.

## Step 3: Use Flask and Heroku to host the tracker online
- Uses Flask to manage the interactivity and display the desired content.
- Hosted on Heroku:
    Visit it at: https://tickertrackerhayes.herokuapp.com/
