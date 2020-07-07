#!/usr/bin/env python3
###############################################################################
# dash-health - functions
# **Copyright (C) 2019 tschinz - All Rights Reserved**
###############################################################################

###############################################################################
# Import sub-modules
# python
import sys
import os
import datetime
import enum
import zipfile
import glob

# iPython
import IPython
from IPython.display import display
from IPython.display import Image

# pandas
import pandas as pd

# numpy
import numpy as np

# plotly
import plotly as ply
import plotly.io as pio
import plotly.graph_objs as go
import plotly.figure_factory as ff
ply.offline.init_notebook_mode(connected=True)

# dash
import dash
import dash_auth
import dash_table
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html

# local project imports
from hevslib.time import *
from hevslib.general import *
from hevslib.pandas import *
from hevslib.plotly import *
from hevslib.applehealth import *
from config import *

###############################################################################
# Custom Import Functions
#


###############################################################################
# Custom Dashboard Plot figures
#
def plotValueVsTime(df, outputDir, title="", measurement=None, plotlySettings=None, rolling_mean=3):
  # plot value vs time
  # .. prepare traces
  trace_value = ply.graph_objs.Scatter(
    x=df.index,
    y=df.value,
    mode='markers',
    name=df_description[measurement],
  )
    
  # .. add a rolling mean to data
  trace_value_mean = ply.graph_objs.Scatter(
    x=df.index,
    y=df.value.rolling(3).mean(),
    mode='lines',
    name="{} Rolling Mean".format(df_description[measurement]),
  )
    
  # .. set layout
  mylayout = ply.graph_objs.Layout(
    title="{}{} vs Time".format(title, df_description[measurement]),
    yaxis=dict(
      title="{}{} [{}]".format(title, df_description[measurement], df.unit[0])
    )
  )
    
  # .. set data to plot
  traces = [trace_value, trace_value_mean]
    
  # .. plot
  graphFilename = outputDir + mylayout.title.text + ' - Scatter vs Time.html'
  fig = ply.graph_objs.Figure(data=traces, layout=mylayout)
  plotFigure(graphFilename, fig, plotlySettings[1], plotlySettings[2], plotlySettings[3], plotlySettings[4])
  print(plotlySettings[1], plotlySettings[2], plotlySettings[3], plotlySettings[4])
  return(fig)


###############################################################################
# Pandas Functions
#
def cleanDf(df, df_info):
  # remove empty columns
  if verbose >= 1:
    print("Dataframe {}".format(df_info))
    print("* Search for empty colums")
  for col in df.columns:
    if df[col].value_counts().sum() <= 0:
      if verbose >= 1:
        print("  * Remove column {}".format(col))
      df.drop([col], axis=1, inplace=True)
  # convert to datetime
  if verbose >= 1:
    print("* Search for date colums")
  for col in df.columns:
    if "date" in col.lower():
      if verbose >= 1:
        print("  * Column {} converted to datetime".format(col))  
      df[col] =  pd.to_datetime(df[col], format='%Y-%m-%d %H:%M:%S', utc=True)
      
      
def cleanDfs(dfs, dfs_info):
  for i in range(len(dfs)):
    cleanDf(dfs[i], dfs_info[i])
  

def valueStats(dfs, dfs_info, i):
  print("\n{}".format(dfs_info[i]))
  print("  * Time between {} - {}".format(dfs[i].startDate.iat[0].strftime("%x %X"), dfs[i].startDate.iat[-1].strftime("%x %X")))
  print("  * Measured by {}".format(dfs[i].sourceName.iat[0]))
  print(dfs_info[i])
  if df_description['sleep'] == dfs_info[i]:
    print("  * {} measurements".format(len(dfs[i].value)))
  elif df_description['workout'] == dfs_info[i]:
    print("  * {} measurements".format(len(dfs[i])))
    print("  * Total duration: {} {}".format(dfs[i].duration.sum(), dfs[i].durationUnit.iat[0]))
    print("  * Total total distance: {} {}".format(dfs[i].totalDistance.sum(), dfs[i].totalDistanceUnit.iat[0]))
    print("  * Total total energy burned: {} {}".format(dfs[i].totalEnergyBurned.sum(), dfs[i].totalEnergyBurnedUnit.iat[0]))
  else:
    print("  * {} measurements".format(len(dfs[i].value)))
    print("  * Total {} {}".format(dfs[i].value.sum(), dfs[i].unit.iat[0]))
    
###############################################################################
# Custom Visualization Functions
#
