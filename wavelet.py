import pywt
import glob
import json
import math

import numpy as np
import plotly.graph_objs as go
import plotly.plotly
import xlrd
from plotly import tools
import pylab
from numpy import arange,array,ones
from scipy import stats
from sklearn.metrics import mean_absolute_error, mean_squared_error

fileName = ""
iroadsFilepath = "iroadsData\\" + fileName + ".json"


array1 =None
with open(iroadsFilepath) as data_file:
    array1 = json.load(data_file)
