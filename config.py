#!/usr/bin/env python3
###############################################################################
# dash-health - config
# **Copyright (C) 2019 tschinz - All Rights Reserved**
###############################################################################
##############################################################################
# Import sub-modules
import os

###############################################################################
# Constants
#
# 0 = no output
# 1 = normal output
# 2 = verbose output
verbose = 2

# Data Storage constants
asset_dir = 'assets'
data_dir = 'data'
csv_file = "20170112-sbb-tunnel.csv"
json_file = "example.json"

###############################################################################
# app variables
#
page_title = 'Streamlit Cheatsheet'
author = 'tschinz'
author_url = 'https://github.com/tschinz'
sidebar_title = 'Controls'
repo = 'github'
repo_url = 'https://github.com/tschinz/streamlit-cheatsheet'
deploy = 'heroku'
deploy_url = 'https://streamlit-cheatsheet.herokuapp.com/'

data = 'OpenData Swiss'
data_url = 'https://opendata.swiss/en/dataset/tunnel1'

footer = "Made with :heart: by [{}]({})".format(author, author_url) + os.linesep
footer += "Source on [{}]({}) deployed at [{}]({})".format(repo, repo_url, deploy, deploy_url) + os.linesep
footer += "Datasource from [{}]({})".format(data, data_url)