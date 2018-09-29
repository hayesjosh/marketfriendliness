#importing (taken from my first flask project)
from flask import Flask, render_template, request, redirect
import requests
import pandas as pd
from bokeh.plotting import figure, output_file, show
from bokeh.embed import components
import os
import json

#importing (taken from bokeh county-map template)
from bokeh.io import show
from bokeh.models import LogColorMapper
from bokeh.palettes import Viridis6 as palette
from bokeh.plotting import figure
from bokeh.sampledata.us_counties import data as counties
from bokeh.sampledata.unemployment import data as unemployment
##imports done



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
    palette.reverse()

    counties = {
        code: county for code, county in counties.items() if county["state"] == "tx"
    }

    county_xs = [county["lons"] for county in counties.values()]
    county_ys = [county["lats"] for county in counties.values()]

    county_names = [county['name'] for county in counties.values()]
    county_rates = [unemployment[county_id] for county_id in counties]
    color_mapper = LogColorMapper(palette=palette)

    data=dict(
        x=county_xs,
        y=county_ys,
        name=county_names,
        rate=county_rates,
    )

    TOOLS = "pan,wheel_zoom,reset,hover,save"

    p = figure(
        title="Texas Unemployment, 2009", tools=TOOLS,
        x_axis_location=None, y_axis_location=None,
        tooltips=[
            ("Name", "@name"), ("Unemployment rate)", "@rate%"), ("(Long, Lat)", "($x, $y)")
        ])
    p.grid.grid_line_color = None
    p.hover.point_policy = "follow_mouse"

    p.patches('x', 'y', source=data,
              fill_color={'field': 'rate', 'transform': color_mapper},
              fill_alpha=0.7, line_color="white", line_width=0.5)

    # user_fico = request.form['credit_input']
    # ##let's graph it in Bokeh!
    # # create a new plot with a title and axis labels
    # p = figure(title="Average Credit Score Across Counties", x_axis_type='datetime', x_axis_label='Date', y_axis_label='$ Value')
    # # add a line renderer with legend and line thickness
    # p.line(jdata['date'], jdata['close'], line_width=2)
    script, div = components(p)
    ##sending user over to the newly made graph.html
    return render_template('graph.html', script=script, div=div)









###closing down
if __name__ == '__main__':
  #port = int(os.environ.get("PORT", 5000))
  #app.run(host='0.0.0.0', port=port)
  app.run(port=33507)
  #app.run(debug=True)
