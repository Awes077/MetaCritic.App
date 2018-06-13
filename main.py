import sqlite3 as sql
import pandas.io.sql as psql
import numpy as np
import bokeh.palettes as bp
from bokeh.plotting import figure, show
from bokeh.layouts import layout, widgetbox
from bokeh.models import ColumnDataSource, Div, HoverTool, DatetimeTickFormatter, Range1d
from bokeh.models.widgets import Slider, Select, TextInput, Tabs
from bokeh.io import curdoc, output_notebook
import pandas as pd


from scripts.Music import music_tab
from scripts.Movies import movie_tab



con = sql.connect('/Users/aaronwestmoreland/Documents/Data.Projects/Music/Metacritic.db')

Movies = psql.read_sql('SELECT * FROM Movies;', con)

#Removing all TBA dates now 
Movies = Movies[Movies["Release"]!="TBA"]



Music = psql.read_sql('SELECT * FROM Music;', con)




tab_1 = music_tab(Music)
tab_2 = movie_tab(Movies)

tabs=Tabs(tabs=[tab_1, tab_2])

curdoc().add_root(tabs)