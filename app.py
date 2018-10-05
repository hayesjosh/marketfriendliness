#importing (taken from my first flask project)
from flask import Flask, render_template, request, redirect
import os
import pickle
import csv
# import feather
# import requests
# import pandas as pd
# #importing (taken from bokeh county-map template)
from bokeh.plotting import figure, output_file, show
from bokeh.embed import components
from bokeh.io import show
from bokeh.models import LogColorMapper
from bokeh.palettes import RdBu10 as palette
from bokeh.plotting import figure


# import xml.etree.cElementTree as et


palette.reverse()
with open('data/county_names.p', 'rb') as fp:
    county_names = pickle.load(fp)
with open('data/county_xs.p', 'rb') as fp:
    county_xs = pickle.load(fp)
with open('data/county_ys.p', 'rb') as fp:
    county_ys = pickle.load(fp)
with open('data/county_fico.p', 'rb') as fp:
    county_fico = pickle.load(fp)
with open('data/county_fthb.p', 'rb') as fp:
    county_fthb = pickle.load(fp)


#starting up our app
app = Flask(__name__)






#the primary page
@app.route('/')
def index():
    return render_template('index.html')












#on click
@app.route('/index',methods=['GET','POST'])
def index_tick():
    color_mapper = LogColorMapper(palette=palette)

    if request.form['credit_input']:
        user_fico = request.form['credit_input']
    else:
        user_fico = 680

    user_diff = [int(user_fico) - x for x in county_fico]

    if request.form['state_input']:
        user_state = request.form['state_input']
    else:
        user_state = "TX"

    data=dict(
        x=county_xs,
        y=county_ys,
        name=county_names,
        fico=county_fico,
        fthb=county_fthb,
        credit_diff=user_diff
    )


    TOOLS = "pan,wheel_zoom,reset,hover,save"

    p = figure(
        title="Housing Market Comparison: "+user_state, tools=TOOLS,
        x_axis_location=None, y_axis_location=None,
        tooltips=[
            ("County Name", "@name"),
            ("Avg. Credit Score", "@fico"),
            ("Your Credit Surplus", "@credit_diff"),
            ("Market Friendliness", "@fthb")
        ])
    p.grid.grid_line_color = None
    p.hover.point_policy = "follow_mouse"

    p.patches('x', 'y', source=data,
              fill_color={'field': 'fthb', 'transform': color_mapper},
              fill_alpha=0.7, line_color="white", line_width=0.5)



    script, div = components(p)
    #sending user over to the newly made graph.html
    return render_template('graph.html', script=script, div=div)


###closing down
if __name__ == '__main__':
  #port = int(os.environ.get("PORT", 5000))
  #app.run(host='0.0.0.0', port=port)
#  app.run(port=33507)
  app.run(port=5000)
  #app.run(debug=True)
