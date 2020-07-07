#!/usr/bin/env python3
###############################################################################
# dash-health - config
# **Copyright (C) 2019 tschinz - All Rights Reserved**
###############################################################################
import pandas as pd
import os
###############################################################################
# Constants
#
# 0 = no output
# 1 = normal output
# 2 = verbose output
verbose = 2

# Data Storage constants
data_inputDir = 'data'
data_tempDir = 'tmp'

###############################################################################
# app variables
#
page_title = 'Streamlit Cheatsheet'
page_subtitle = 'tschinz'
tab_title = 'Streamlit'
github_url = 'https://github.com/tschinz/dash-health'
data_url = 'https://agp.hes-so.ch'
flaticon_author = ["Freepik", "https://www.flaticon.com/authors/freepik"]
flaticon = ["Flaticon", "https://www.flaticon.com"]

# Controls
duration_dropdown = {
  'R': 'Range',
  'A': 'All',
}
project_dropdown = {}

# Keep this out of source code repository - save in a file or a database
login_credentials = {
  'dash-health': '4ZB2PVLEhYHRcwzCyvJr'
}

df_description = {
  'energy': "ActiveEnergyBurned",
  'alcohol': "BloodAlcoholContent",
  'fat': "BodyFatPercentage",
  'weight': "BodyMass",
  'bmi': "BodyMassIndex",
  'caffeine': "DietaryCaffeine",
  'water': "DietaryWater",
  'cycling': "DistanceCycling",
  'walking': "DistanceWalkingRunning",
  'flightsclimbed': "FlightsClimbed",
  'heartrate': "HeartRate",
  'height': "Height",
  'sleep': "SleepAnalysis",
  'steps': "StepCount",
  'workout': "Workout"
}

###############################################################################
# Graph output Options
#
#notebookGraphicInteraction = GraphInteractionOption('interactive')
notebookGraphicInteraction = GraphInteractionOption('static')
notebookGraphicOutputs = GraphOutputOption('both')

ext_file = ".svg"

staticImageSize = {'width': 1000, 'height': 500, 'scale': 1}

GraphAutoOpenHTML = False  # Auto open external HTML files [True/False]

plotlySettings = [ext_file, staticImageSize, notebookGraphicOutputs, notebookGraphicInteraction, GraphAutoOpenHTML]
