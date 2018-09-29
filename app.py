#importing
from flask import Flask, render_template, request, redirect
import requests
import pandas as pd
from bokeh.plotting import figure, output_file, show
from bokeh.embed import components
import os
import json

#starting up our app
app = Flask(__name__)

#the primary page
@app.route('/')
def index():
  return render_template('index.html')

#on click
@app.route('/index',methods=['GET','POST'])
def index_tick():
    ####Request was POST, let's use that info to make a custom graph!
    ###Let's set up a webscrape, clean the data, and graph it!
    ##Setting up the webscrape
    #A little function that accepts 'ticker' 'start_date' and 'end_date' and concats them into a url
    def urldefine(ticker, start_date, end_date):
        seq = ("https://www.quandl.com/api/v3/datasets/WIKI/"+ticker+".json?start_date="+start_date+"&end_date="+end_date+"&api_key=TQ15R7SeyT-_W-bqEDJY")
        return seq
    #bringing over the user input
    ticker_1 = request.form['ticker_input']
    #ideally this will be user input or update automatically, but for now, let's use these defaults to test
    start_date_1 = '2017-08-07'
    end_date_1 = '2017-09-07'
    #Creating the custom URL
    url_2 = urldefine(ticker_1, start_date_1, end_date_1)

    ##Actually requesting the data from that URL
    r = requests.get(url_2)
    #putting the returned web info into python-- i.e. translating the json data
    j1 = r.json()

    ##Now let's put it in a dataframe and clean it up!
    #create column names
    cols = ['date','open','high','low','close','volume','dividend','split','adj_open','adj_high','adj_low','adj_close','adj_volume']
    #now lets load it into a dataframe
    jdata = pd.DataFrame(j1['dataset']['data'], columns = cols)
    #Gotta change the date variable format
    jdata['date'] = pd.to_datetime(jdata['date'], format= '%Y-%m-%d')
    ##let's graph it in Bokeh!
    # output to static HTML file
    #output_file("templates/graphs.html")
    # create a new plot with a title and axis labels
    p = figure(title=ticker_1+" Stock Tracker: Value at Closing", x_axis_type='datetime', x_axis_label='Date', y_axis_label='$ Value')
    # add a line renderer with legend and line thickness
    p.line(jdata['date'], jdata['close'], line_width=2)
    # show the results
    #show(p)
    script, div = components(p)
    ##sending user over to the newly made graph.html
    return render_template('graph.html', script=script, div=div)
    #return redirect('graphs.html')

if __name__ == '__main__':
  #port = int(os.environ.get("PORT", 5000))
  #app.run(host='0.0.0.0', port=port)
  app.run(port=33507)
  #app.run(debug=True)
