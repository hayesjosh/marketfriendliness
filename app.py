from flask import Flask, render_template, request, redirect
import os
import pickle
import csv
from bokeh.plotting import figure, output_file, show
from bokeh.embed import components
from bokeh.io import show
from bokeh.models import LogColorMapper, LogTicker, ColorBar, FixedTicker, BasicTicker, PrintfTickFormatter, LinearColorMapper
from bokeh.palettes import YlGn9  as fthb_palette
from bokeh.palettes import Reds9 as fico_palette
from bokeh.palettes import RdBu10 as fico_diff_palette
from bokeh.plotting import figure

fthb_palette.reverse()
fico_palette.reverse()
fico_diff_palette.reverse()

with open('data/graph_data.p', 'rb') as fp:
    graph_data = pickle.load(fp)

#starting up our app
app = Flask(__name__)

#the primary page
@app.route('/')
def index():
    state_list = ['WV', 'OH', 'GA', 'KS', 'CA', 'UT', 'MD', 'PA', 'FL', 'AZ', 'NY', 'MA', 'MN', 'WI', 'CT', 'WA', 'SC','TX', 'MT', 'CO', 'TN', 'IA', 'NM', 'IN', 'ME', 'VA', 'MO', 'NC', 'OR', 'NV', 'IL', 'KY', 'MS', 'ND', 'NE', 'LA', 'NH', 'AL', 'RI', 'ID', 'OK','SD', 'AR', 'HI', 'VT', 'WY', 'DE']
    color_list = ['fico','fthb','credit_diff']
    state_list.sort()
    return render_template('index.html', state_list = state_list, color_list = color_list)

#on click
@app.route('/index',methods=['GET','POST'])
def graph():
    #bringing over user input from the website
    if request.form.get('state_dropdown'):
        user_state2 = request.form.get('state_dropdown')
    else:
        user_state2 = "TX"

    #getting appropriate data
    state_data = graph_data[user_state2]
    county_names = state_data[0]
    county_xs= state_data[1]
    county_ys = state_data[2]
    county_fico = state_data[3]
    county_fthb = state_data[4]

    if request.form['credit_input']:
        user_fico = request.form['credit_input']
    else:
        user_fico = 720

    #calculating fico differences based on user input
    user_diff = [int(user_fico) - x for x in county_fico]

    #bringing in the graph colorization type
    if request.form.get('color_dropdown'):
        graph_type = request.form.get('color_dropdown')
    else:
        graph_type = "fico"

    #building dict for graphing
    data=dict(
        x=county_xs,
        y=county_ys,
        name=county_names,
        fico=county_fico,
        fthb=county_fthb,
        credit_diff=user_diff
    )

    TOOLS = "pan,wheel_zoom,reset,hover,save"

#DIFFERENT GRAPH TYPES BELOW
    if graph_type == 'fico':
        min_value = min(county_fico)
        max_value = max(county_fico)
        color_mapper = LinearColorMapper(palette=fico_palette, low=min_value, high=max_value)
        p = figure(
            title="Housing Market Comparison: "+user_state2+" | Color showing: Average FICO Score Predictions", tools=TOOLS,
            x_axis_location=None, y_axis_location=None,
            tooltips=[
                ("County Name", "@name"),
                ("Avg. Credit Score", "@fico"),
                ("Your Credit Surplus", "@credit_diff"),
                ("First-Time Buyer %", "@fthb")
                # ("Market Friendliness", "@fthb")
            ])
        p.grid.grid_line_color = None
        p.hover.point_policy = "follow_mouse"

        p.patches('x', 'y', source=data,
                  fill_color={'field': graph_type, 'transform': color_mapper},
                  # fill_color={'field': 'fthb', 'transform': color_mapper},
                  fill_alpha=0.7, line_color="white", line_width=0.5)

        color_bar = ColorBar(color_mapper=color_mapper, ticker=BasicTicker(desired_num_ticks=10),
                         label_standoff=12, border_line_color=None, location=(0,0))

        p.add_layout(color_bar, 'right')

        script, div = components(p)

    elif graph_type == 'credit_diff':
        min_value = min(user_diff)
        max_value = max(user_diff)
        color_mapper = LinearColorMapper(palette=fico_diff_palette, low=-40, high=40)
        p = figure(
            title="Housing Market Comparison: "+user_state2+" | Color showing: FICO Surplus compared to Predictions", tools=TOOLS,
            x_axis_location=None, y_axis_location=None,
            tooltips=[
                ("County Name", "@name"),
                ("Avg. Credit Score", "@fico"),
                ("Your Credit Surplus", "@credit_diff"),
                ("First-Time Buyer %", "@fthb")
                # ("Market Friendliness", "@fthb")
            ])
        p.grid.grid_line_color = None
        p.hover.point_policy = "follow_mouse"

        p.patches('x', 'y', source=data,
                  fill_color={'field': graph_type, 'transform': color_mapper},
                  # fill_color={'field': 'fthb', 'transform': color_mapper},
                  fill_alpha=0.7, line_color="white", line_width=0.5)

        color_bar = ColorBar(color_mapper=color_mapper, ticker=BasicTicker(desired_num_ticks=10),
                         label_standoff=12, border_line_color=None, location=(0,0))

        p.add_layout(color_bar, 'right')

        script, div = components(p)

    else:
        min_value = min(county_fthb)
        max_value = max(county_fthb)
        color_mapper = LinearColorMapper(palette=fthb_palette, low=min_value, high=max_value)

        p = figure(
            title="Housing Market Comparison: "+user_state2+" | Color showing: First-Time Home Buyer % Predictions", tools=TOOLS,
            x_axis_location=None, y_axis_location=None,
            tooltips=[
                ("County Name", "@name"),
                ("Avg. Credit Score", "@fico"),
                ("Your Credit Surplus", "@credit_diff"),
                ("First-Time Buyer %", "@fthb")
                # ("Market Friendliness", "@fthb")
            ])
        p.grid.grid_line_color = None
        p.hover.point_policy = "follow_mouse"

        p.patches('x', 'y', source=data,
                  fill_color={'field': graph_type, 'transform': color_mapper},
                  # fill_color={'field': 'fthb', 'transform': color_mapper},
                  fill_alpha=0.7, line_color="white", line_width=0.5)

        color_bar = ColorBar(color_mapper=color_mapper, ticker=BasicTicker(desired_num_ticks=11),
                         formatter=PrintfTickFormatter(format="%d%%"), label_standoff=12, location=(0,0))

        p.add_layout(color_bar, 'right')

        script, div = components(p)
    #sending user over to the newly made graph.html
    return render_template('graph.html', script=script, div=div)

#the about page
@app.route('/about')
def about():
    return render_template('about.html')

#the method page
@app.route('/method')
def method():
    return render_template('method.html')

###closing down
if __name__ == '__main__':
  #port = int(os.environ.get("PORT", 5000))
  #app.run(host='0.0.0.0', port=port)
#  app.run(port=33507)
  app.run(port=5000)
  # app.run(port=5000, debug=True)
