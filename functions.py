#!/usr/bin/env python3
###############################################################################
# streamlit-cheatsheet - functions
# **Copyright (C) 2019 tschinz - All Rights Reserved**
###############################################################################

###############################################################################
# Import sub-modules
# python
import os

# pandas
import pandas as pd

# numpy
import numpy as np

# plotly
import plotly as ply
import plotly.io as pio
import plotly.graph_objs as go
import plotly.figure_factory as ff

# streamlit
import streamlit as st

# local project imports
from config import *

def createDir(directory, verbose=0):
  """Checks if directory exists, and creates it if not

  Args:
      dir: string location of directory
      verbose: integer for verbosity
  Returns:
      None
  Raises:
      NotADirectoryError
  """
  if (os.path.exists(directory)) is False:
    os.makedirs(directory)
    if verbose >= 2:
      print("Directory {} created".format(directory))
  if (os.path.isdir(directory)) is False:
    raise NotADirectoryError("{} is not a directory".format(directory))


###############################################################################
# Custom Import Functions
#

###############################################################################
# Pandas Functions
#

###############################################################################
# Custom Visualization Functions
#
