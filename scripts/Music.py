#! /usr/bin/python

import sqlite3 as sql
import pandas.io.sql as psql
import numpy as np
import bokeh.palettes as bp
from bokeh.plotting import figure, show
from bokeh.layouts import layout, widgetbox
from bokeh.models import ColumnDataSource, Div, HoverTool, DatetimeTickFormatter, Panel
from bokeh.models.widgets import Slider, Select, TextInput
from bokeh.io import curdoc, output_notebook
import pandas as pd


def music_tab(Music):

	def make_dataset(Music):
		#con = sql.connect('/Users/aaronwestmoreland/Documents/Data.Projects/Music/Metacritic.db')

	

	#Music = psql.read_sql('SELECT * FROM Music;', con)
	
		Mus_split=Music["Day"].str.split(' ', expand=True)
		Music["Month"]=Mus_split[0]
		Music["Date"]=Mus_split[1]
		
		c_map = bp.magma(len(np.unique(Music["Score"])))
		c_dict = zip( np.unique(Music["Score"]), c_map)
		Col_MAP = dict(c_dict)
		Music["color"]= Music["Score"].apply(lambda x: Col_MAP[x])

	#Music["Month"]


		Music["DateTime"]= pd.to_datetime(Music["Release"],format="%b %d, %Y")




		Music['alpha'] = np.where(Music["Score"].astype(float)>=90, 0.9, 0.25)

		mu_dict = dict(x=Music["Release"], y=Music["Score"].astype(float), album=Music["Album"], 
		release=Music["Release"], artist=Music["Artist"], alpha=Music["alpha"],
		color=Music['color'],)
		return ColumnDataSource(mu_dict)
	

	def make_plot(src):
		axis_map = {
			"Year": "DateTime",
			"MetaCritic Score": "Score",
			}

		x_axis = Select(title="X Axis", options=sorted(axis_map.keys()), value="Year")
		y_axis = Select(title="Y Axis", options=sorted(axis_map.keys()), value="MetaCritic Score")

		TOOLTIPS = [
			("Album","@album"),
			("Artist", "@artist"),
			("Score", "@y"),
			("Release", "@release")
			]	

		p = figure(plot_height=600, plot_width=700, title="", toolbar_location="below", x_axis_type="datetime")
		p.circle(x="x", y="y", source=src, size=7, color="color", line_color=None, fill_alpha="alpha")
		p.add_tools(HoverTool(show_arrow=False, line_policy='next', tooltips=TOOLTIPS))
		p.xaxis.formatter=DatetimeTickFormatter(
			hours=["%d %B %Y"],
			days=["%d %B %Y"],
			months=["%d %B %Y"],
			years=["%d %B %Y"],)
	
		p.xaxis.major_label_orientation = np.pi/4
		return p, axis_map, y_axis, x_axis
	


	def select_Music():
		Month_val = Month.value
		selected = Music
		if(Month_val != "All"):
			selected = selected[selected.Month.str.contains(Month_val)==True]
		return selected





	def update():
		df = select_Music()
		x_name = axis_map[x_axis.value]
		y_name = axis_map[y_axis.value]
	
		p.xaxis.axis_label = x_axis.value
		p.yaxis.axis_label = y_axis.value
		p.title.text = "%d Albums selected" % len(df)
		src.data = dict(
			x=df[x_name],
			y=df[y_name].astype(float),
			album = df["Album"],
			release= df["Release"],
			artist = df["Artist"],
			alpha = df["alpha"],
			color = df["color"],)

	src=make_dataset(Music)
	months=list(np.unique(Music["Month"]))
	months.append("All")
	
	Month = Select(title="Release Month",value="All", options=months)
	
	
	p, axis_map, y_axis, x_axis=make_plot(src)
	
	controls = [Month]
	for control in controls:
		control.on_change('value', lambda attr, old, new: update())

	
	sizing_mode = 'fixed'

	inputs = widgetbox(*controls, sizing_mode=sizing_mode)
	l= layout([
		[inputs, p]
	], sizing_mode = sizing_mode)



	update()
	tab = Panel(child=l, title="Music")
	return tab



#curdoc().add_root(l)
#curdoc().title = "Music"

