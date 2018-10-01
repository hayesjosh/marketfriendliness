#importing (taken from my first flask project)
from flask import Flask, render_template, request, redirect
import feather
# import requests
# import pandas as pd
# from bokeh.plotting import figure, output_file, show
# from bokeh.embed import components
import os
# import json
#
# #importing (taken from bokeh county-map template)
from bokeh.io import show
from bokeh.models import LogColorMapper
from bokeh.palettes import Viridis6 as palette
from bokeh.plotting import figure
# from bokeh.sampledata.us_counties import data as counties
# from bokeh.sampledata.unemployment import data as unemployment
# ##imports done

#importing (taken from bokeh sample data)
import csv
import xml.etree.cElementTree as et

#code to find counties Data
def external_path(filename):
    data_dir = "data/"
    fn = join(data_dir, filename)
    if not exists(fn) and isfile(fn):
        raise RuntimeError('Could not locate external data file %e. Please execute bokeh.sampledata.download()' % fn)
    return fn
#code to open csv
def open_csv(filename):
    '''
    '''
    # csv differs in Python 2.x and Python 3.x. Open the file differently in each.
    if six.PY2:
        return open(filename, 'rb')
    else:
        return open(filename, 'r', newline='', encoding='utf8')


#code to read in the counties data
def _read_data():
    '''
    '''
    nan = float('NaN')

    data = {}

    with open_csv(external_path('US_Counties.csv')) as f:
        next(f)
        reader = csv.reader(f, delimiter=str(','), quotechar=str('"'))
        for row in reader:
            name, dummy, state, dummy, geometry, dummy, dummy, dummy, det_name, state_id, county_id, dummy, dummy = row
            xml = et.fromstring(geometry)
            lats = []
            lons = []
            for i, poly in enumerate(xml.findall('.//outerBoundaryIs/LinearRing/coordinates')):
                if i > 0:
                    lats.append(nan)
                    lons.append(nan)
                coords = (c.split(',')[:2] for c in poly.text.split())
                lat, lon = list(zip(*[(float(lat), float(lon)) for lon, lat in
                    coords]))
                lats.extend(lat)
                lons.extend(lon)
            data[(int(state_id), int(county_id))] = {
                'name' : name,
                'detailed name' : det_name,
                'state' : state,
                'lats' : lats,
                'lons' : lons,
            }

    return data




    counties = _read_data()



    counties = {
        code: county for code, county in counties.items() if county["state"] == "tx"
    }







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

    #
    # county_xs = [county["lons"] for county in counties.values()]
    # county_ys = [county["lats"] for county in counties.values()]
    #
    # county_names = [county['name'] for county in counties.values()]
    # county_rates = [unemployment[county_id] for county_id in counties]
    # color_mapper = LogColorMapper(palette=palette)
    #
    # data=dict(
    #     x=county_xs,
    #     y=county_ys,
    #     name=county_names,
    #     rate=county_rates,
    # )
    #
    # TOOLS = "pan,wheel_zoom,reset,hover,save"
    #
    # p = figure(
    #     title="Texas Unemployment, 2009", tools=TOOLS,
    #     x_axis_location=None, y_axis_location=None,
    #     tooltips=[
    #         ("Name", "@name"), ("Unemployment rate)", "@rate%"), ("(Long, Lat)", "($x, $y)")
    #     ])
    # p.grid.grid_line_color = None
    # p.hover.point_policy = "follow_mouse"
    #
    # p.patches('x', 'y', source=data,
    #           fill_color={'field': 'rate', 'transform': color_mapper},
    #           fill_alpha=0.7, line_color="white", line_width=0.5)
    #
    # # user_fico = request.form['credit_input']
    # # ##let's graph it in Bokeh!
    # # # create a new plot with a title and axis labels
    # # p = figure(title="Average Credit Score Across Counties", x_axis_type='datetime', x_axis_label='Date', y_axis_label='$ Value')
    # # # add a line renderer with legend and line thickness
    # # p.line(jdata['date'], jdata['close'], line_width=2)
    # script, div = components(p)
    ##sending user over to the newly made graph.html
    return render_template('graph.html', script=script, div=div)


###closing down
if __name__ == '__main__':
  #port = int(os.environ.get("PORT", 5000))
  #app.run(host='0.0.0.0', port=port)
  app.run(port=33507)
  #app.run(debug=True)
