import json
import math
import xlrd
from plotly import tools
import plotly.plotly
import plotly.graph_objs as go
import numpy as np
import glob
import math
fig = tools.make_subplots(rows=1, cols=3, shared_yaxes=True)

iroadsFilepath = "iroadsData\\" + "sir" + ".json"
array1 = None
with open(iroadsFilepath) as data_file:
    array1 = json.load(data_file)
timeArray = []
acceYArray = []

time0 = array1[0]["time"]

for idx,item in enumerate(array1):
        timeArray.append(item["time"]-time0)
        acceYArray.append(item["acceY"])

traceStill = go.Scatter(
        x= timeArray,
        y=acceYArray,
        mode='lines',
        name="Engine Not Started"
    )
fig.append_trace(traceStill, 1, 1)

iroadsFilepath = "iroadsData\\" + "engineStartedSpeed0" + ".json"
array1 = None
with open(iroadsFilepath) as data_file:
    array1 = json.load(data_file)
timeArray = []
acceYArray = []

time0 = array1[0]["time"]

for idx,item in enumerate(array1):
    if idx <250:
        timeArray.append(item["time"]-time0)
        acceYArray.append(item["acceX_raw"])

traceStill = go.Scatter(
        x= timeArray,
        y=acceYArray,
        mode='lines',
        name="Engine Started Speed 0"
    )
fig.append_trace(traceStill, 1, 2)

iroadsFilepath = "iroadsData\\" + "galleRoadToCastleRoad" + ".json"
array1 = None
with open(iroadsFilepath) as data_file:
    array1 = json.load(data_file)
timeArray = []
acceYArray = []

time0 = array1[0]["time"]

for idx,item in enumerate(array1):
    if idx <250:
        timeArray.append(item["time"]-time0)
        acceYArray.append(item["acceX_raw"])

traceStill = go.Scatter(
        x= timeArray,
        y=acceYArray,
        mode='lines',
        name="Normal Ride"
    )
fig.append_trace(traceStill, 1, 3)

fig['layout'].update(height=600, width=1500,xaxis=dict(
        title='Time(ms)',
        titlefont=dict(
            family='Courier New, monospace',
            size=18,
            color='#7f7f7f'
        )
    ),
    yaxis=dict(
        title='Acceleration Y (m/s2)',
        titlefont=dict(
            family='Courier New, monospace',
            size=18,
            color='#7f7f7f'
        )))
plotly.offline.plot(fig, filename='graphsX.html')