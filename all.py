import glob
import json
import math
import csv
import numpy as np
import plotly.graph_objs as go
import plotly.plotly
import xlrd
from plotly import tools
import pylab
from numpy import arange,array,ones
from scipy import stats
from sklearn.metrics import mean_absolute_error, mean_squared_error

romdasSpikes = []
calcSpikes = []
calcSpikesX = []
iri = []
meanY = []
sdY = []
meanX = []
sdX = []
meanZ = []
sdZ = []
romLog = []
iroadLog = []
speed = []

with open('iridata300T.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        # romdasSpikes.append(float(row["romdasSpikes"]))
        calcSpikes.append(float(row["calcSpikesY"]))
        calcSpikesX.append(float(row["calcSpikesX"]))
        iri.append(float(row["iri"]))
        # meanY.append(row["meanY"])
        # sdY.append(row["sdY"])
        # meanX.append(row["meanX"])
        # sdX.append(row["sdX"])
        # meanZ.append(row["meanZ"])
        # sdZ.append(row["sdZ"])
        # romLog.append(row["romLog"])
        # iroadLog.append(row["iroadLog"])
        speed.append(float(row["speed"]))

array10 = []
array1020 = []
array2030 = []
array3040 = []
array4050 = []
array50 = []

arrayA10 = []
arrayA1020 = []
arrayA2030 = []
arrayA3040 = []
arrayA4050 = []
arrayA50 = []
for idx, val in enumerate(speed):
    if val <= 10:
        array10.append(calcSpikes[idx])
        arrayA10.append(iri[idx])

    elif val > 10 and val <= 20:
        array1020.append(calcSpikes[idx])
        arrayA1020.append(iri[idx])

    elif val > 20 and val <= 30:
        array2030.append(calcSpikes[idx])
        arrayA2030.append(iri[idx])

    elif val > 30 and val <= 40:
        array3040.append(calcSpikes[idx])
        arrayA3040.append(iri[idx])
    elif val > 40 and val <= 50:
        array4050.append(calcSpikes[idx])
        arrayA4050.append(iri[idx])

    else:
        array50.append(calcSpikes[idx])
        arrayA50.append(iri[idx])



sampleArray = [0, 100]

slope, intercept, r_value, p_value, std_err = stats.linregress(np.array(array10), np.array(arrayA10))
line = slope * np.array(sampleArray) + intercept

slope1, intercept1, r_value1, p_value1, std_err1 = stats.linregress(np.array(array1020), np.array(arrayA1020))
line1 = slope1 * np.array(sampleArray) + intercept1

slope2, intercept2, r_value2, p_value2, std_err2 = stats.linregress(np.array(array2030), np.array(arrayA2030))
line2 = slope2 * np.array(sampleArray) + intercept2

slope3, intercept3, r_value3, p_value3, std_err3 = stats.linregress(np.array(array3040), np.array(arrayA3040))
line3 = slope3 * np.array(sampleArray) + intercept3

slope4, intercept4, r_value4, p_value4, std_err4 = stats.linregress(np.array(array4050), np.array(arrayA4050))
line4 = slope4 * np.array(sampleArray) + intercept4

slope5, intercept5, r_value5, p_value5, std_err5 = stats.linregress(np.array(array50), np.array(arrayA50))
line5 = slope5 * np.array(sampleArray) + intercept5

fig = tools.make_subplots(rows=1, cols=6, shared_yaxes=True)
dataGraphs = []

#


calcSpikes = []
calcSpikesX = []
iri = []
speed = []

with open('iridata300P.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        # romdasSpikes.append(float(row["romdasSpikes"]))
        calcSpikes.append(float(row["calcSpikesY"]))
        calcSpikesX.append(float(row["calcSpikesX"]))
        iri.append(float(row["iri"]))
        # meanY.append(row["meanY"])
        # sdY.append(row["sdY"])
        # meanX.append(row["meanX"])
        # sdX.append(row["sdX"])
        # meanZ.append(row["meanZ"])
        # sdZ.append(row["sdZ"])
        # romLog.append(row["romLog"])
        # iroadLog.append(row["iroadLog"])
        speed.append(float(row["speed"]))

array10 = []
array1020 = []
array2030 = []
array3040 = []
array4050 = []
array50 = []

arrayA10 = []
arrayA1020 = []
arrayA2030 = []
arrayA3040 = []
arrayA4050 = []
arrayA50 = []
for idx, val in enumerate(speed):
    if val <= 10:
        array10.append(calcSpikes[idx])
        arrayA10.append(iri[idx])

    elif val > 10 and val <= 20:
        array1020.append(calcSpikes[idx])
        arrayA1020.append(iri[idx])

    elif val > 20 and val <= 30:
        array2030.append(calcSpikes[idx])
        arrayA2030.append(iri[idx])

    elif val > 30 and val <= 40:
        array3040.append(calcSpikes[idx])
        arrayA3040.append(iri[idx])
    elif val > 40 and val <= 50:
        array4050.append(calcSpikes[idx])
        arrayA4050.append(iri[idx])

    else:
        array50.append(calcSpikes[idx])
        arrayA50.append(iri[idx])

corReCOEFF = np.corrcoef(arrayA10, array10)[0][1]
trace = go.Scatter(
    x=array10,
    y=arrayA10,
    mode='markers',
    name=" speed < 10 Cor= " + str(corReCOEFF)
    )
fig.append_trace(trace, 1, 1)
corReCOEFF = np.corrcoef(arrayA1020, array1020)[0][1]
trace1 = go.Scatter(
    x= array1020,
    y=arrayA1020,
    mode='markers',
    name="  10 < speed < 20 Cor= " + str(corReCOEFF)
    )
fig.append_trace(trace1, 1, 2)
corReCOEFF = np.corrcoef(arrayA2030, array2030)[0][1]
trace2 = go.Scatter(
    x=array2030,
    y= arrayA2030,
    mode='markers',
    name=" 20 < speed < 30 Cor= " + str(corReCOEFF)
    )
fig.append_trace(trace2, 1, 3)
corReCOEFF = np.corrcoef(arrayA3040, array3040)[0][1]
trace3 = go.Scatter(
    x=array3040,
    y= arrayA3040,
    mode='markers',
    name=" 30 < speed < 40 Cor= " + str(corReCOEFF)
    )
fig.append_trace(trace3, 1, 4)
corReCOEFF = np.corrcoef(arrayA4050, array4050)[0][1]
trace45 = go.Scatter(
    x= array4050,
    y=arrayA4050,
    mode='markers',
    name="40 < speed < 50 Cor= " + str(corReCOEFF)
    )
fig.append_trace(trace45, 1, 5)
corReCOEFF = np.corrcoef(arrayA50, array50)[0][1]
trace4 = go.Scatter(
    x= array50,
    y=arrayA50,
    mode='markers',
    name=" speed > 40 cor= " + str(corReCOEFF)
    )
fig.append_trace(trace4, 1, 6)


calculatedIRI = slope * np.array(array10) + intercept
# mean_absolute_error11=mean_absolute_error(np.array(arrayA10), calculatedIRI)
# traceLine = go.Scatter(
#     x=sampleArray,
#     y=line,
#     mode='lines',
#     name=str(round(mean_absolute_error11,5))
# )
# fig.append_trace(traceLine, 1, 1)

calculatedIRI1 = slope1 * np.array(array1020) + intercept1
print(calculatedIRI1)
mean_absolute_error1=mean_absolute_error(np.array(arrayA1020), calculatedIRI1)
traceLine1 = go.Scatter(
    x=sampleArray,
    y=line1,
    mode='lines',
    name=str(round(mean_absolute_error1,5))
)
fig.append_trace(traceLine1, 1, 2)

calculatedIRI2= slope2 * np.array(array2030) + intercept2
mean_absolute_error2=mean_absolute_error(arrayA2030, calculatedIRI2)
traceLine2 = go.Scatter(
    x=sampleArray,
    y=line2,
    mode='lines',
    name=str(round(mean_absolute_error2,5))
)
fig.append_trace(traceLine2, 1, 3)

calculatedIRI3 = slope3 * np.array(array3040) + intercept3
mean_absolute_error3=mean_absolute_error(arrayA3040, calculatedIRI3)
traceLine3 = go.Scatter(
    x=sampleArray,
    y=line3,
    mode='lines',
    name=str(round(mean_absolute_error3,5))
)
fig.append_trace(traceLine3, 1, 4)

calculatedIRI4 = slope4 * np.array(array4050) + intercept4
mean_absolute_error4=mean_absolute_error(arrayA4050, calculatedIRI4)
traceLine4 = go.Scatter(
    x=sampleArray,
    y=line4,
    mode='lines',
    name=str(round(mean_absolute_error4,5))
)
fig.append_trace(traceLine4, 1, 5)

calculatedIRI5 = slope5 * np.array(array50) + intercept5
mean_absolute_error5=mean_absolute_error(arrayA50, calculatedIRI5)
traceLine5 = go.Scatter(
    x=sampleArray,
    y=line5,
    mode='lines',
    name=str(round(mean_absolute_error5,5))
)
fig.append_trace(traceLine5, 1, 6)
fig['layout']['xaxis1'].update(title="0<speed<10km/h",range=sampleArray)
fig['layout']['xaxis2'].update(title="10<speed<20km/h",range=sampleArray)
fig['layout']['xaxis3'].update(title="20<speed<30km/h",range=sampleArray)
fig['layout']['xaxis4'].update(title="30<speed<40km/h",range=sampleArray)
fig['layout']['xaxis5'].update(title="40<speed<50km/h",range=sampleArray)
fig['layout']['xaxis6'].update(title="50<speed",range=sampleArray)

fig['layout']['yaxis'].update(title="Iroads Pulse Count")

fig['layout'].update(height=600, width=1500,)
plotly.offline.plot(fig, filename='graphsSpeeds500.html')

allCalculatedData = np.array([])
allCalculatedData = np.append(allCalculatedData,calculatedIRI)
allCalculatedData = np.append(allCalculatedData,calculatedIRI1)
allCalculatedData = np.append(allCalculatedData,calculatedIRI2)
allCalculatedData = np.append(allCalculatedData,calculatedIRI3)
allCalculatedData = np.append(allCalculatedData,calculatedIRI4)
allCalculatedData = np.append(allCalculatedData,calculatedIRI5)
allIRIData = np.array([])
allIRIData = np.append(allIRIData,arrayA10)
allIRIData = np.append(allIRIData,arrayA1020)
allIRIData = np.append(allIRIData,arrayA2030)
allIRIData = np.append(allIRIData,arrayA3040)
allIRIData = np.append(allIRIData,arrayA4050)
allIRIData = np.append(allIRIData,arrayA50)

count123 = []
for idx,i in enumerate(allIRIData):
    count123.append(idx+1)
spikesGraphs = []
traceActual = go.Scatter(
        x=count123,
        y=allIRIData,
        mode='lines',
        name="Actual"
    )
traceCalc = go.Scatter(
        x=count123,
        y=allCalculatedData,
        mode='lines',
        name="Calculated"
    )
spikesGraphs.append(traceActual)
spikesGraphs.append(traceCalc)


plotly.offline.plot({
        "data": spikesGraphs,
        "layout": go.Layout(title="Ac vs CAL All ")
}, auto_open=True, filename='actualVSPredictedIRI100.html')

mean_absolute_error111=mean_absolute_error(allIRIData, allCalculatedData)
print("mean_absolute_error")
print(mean_absolute_error111)


#
#
# fig1 = tools.make_subplots(rows=1, cols=6, shared_yaxes=True)
# allDataIRI1 = np.array(arrayA10)
# allDataCalcSpikesY1 = np.array(array10)
# slope, intercept, r_value, p_value, std_err = stats.linregress(allDataCalcSpikesY1, allDataIRI1)
# title = "y=" + str(round(slope,3)) +"x+" + str(round(intercept,3)) +"///"+ str(round(std_err,3))+"//"+str(round(r_value,3))
# calculatedIRI1 = slope * np.array(array10) + intercept
# mean_absolute_error1=mean_absolute_error(allDataIRI1, calculatedIRI1)
#
# trace1 = go.Scatter(
#     x=calculatedIRI1,
#     y=allDataIRI1,
#     mode='markers',
#     name='Data'
# )
# fig1.append_trace(trace1, 1, 1)
#
#
# allDataIRI2 = np.array(arrayA1020)
# allDataCalcSpikesY2 = np.array(array1020)
# slope, intercept, r_value, p_value, std_err = stats.linregress(allDataCalcSpikesY2, allDataIRI2)
# title = "y=" + str(round(slope,3)) +"x+" + str(round(intercept,3)) +"///"+ str(round(std_err,3))+"//"+str(round(r_value,3))
# calculatedIRI2 = slope * np.array(array1020) + intercept
# mean_absolute_error2=mean_absolute_error(allDataIRI2, calculatedIRI2)
#
# trace2 = go.Scatter(
#     x=calculatedIRI2,
#     y=allDataIRI2,
#     mode='markers',
#     name=str(round(r_value,3))
# )
# fig1.append_trace(trace2, 1, 2)
#
#
# allDataIRI3 = np.array(arrayA2030)
# allDataCalcSpikesY3 = np.array(array2030)
# slope, intercept, r_value, p_value, std_err = stats.linregress(allDataCalcSpikesY3, allDataIRI3)
# title = "y=" + str(round(slope,3)) +"x+" + str(round(intercept,3)) +"///"+ str(round(std_err,3))+"//"+str(round(r_value,3))
# calculatedIRI3 = slope * np.array(array2030) + intercept
# mean_absolute_error3=mean_absolute_error(allDataIRI3, calculatedIRI3)
#
# trace3 = go.Scatter(
#     x=calculatedIRI3,
#     y=allDataIRI3,
#     mode='markers',
#     name=str(round(r_value,3))
# )
# fig1.append_trace(trace3, 1, 3)
#
#
# allDataIRI4 = np.array(arrayA3040)
# allDataCalcSpikesY4 = np.array(array3040)
# slope, intercept, r_value, p_value, std_err = stats.linregress(allDataCalcSpikesY4, allDataIRI4)
# title = "y=" + str(round(slope,3)) +"x+" + str(round(intercept,3)) +"///"+ str(round(std_err,3))+"//"+str(round(r_value,3))
# calculatedIRI4 = slope * np.array(array3040) + intercept
# mean_absolute_error4=mean_absolute_error(allDataIRI4, calculatedIRI4)
#
# trace4 = go.Scatter(
#     x=calculatedIRI4,
#     y=allDataIRI4,
#     mode='markers',
#     name=str(round(r_value,3))
# )
# fig1.append_trace(trace4, 1, 4)
#
#
# allDataIRI5 = np.array(arrayA4050)
# allDataCalcSpikesY5 = np.array(array4050)
# slope, intercept, r_value, p_value, std_err = stats.linregress(allDataCalcSpikesY5, allDataIRI5)
# title = "y=" + str(round(slope,3)) +"x+" + str(round(intercept,3)) +"///"+ str(round(std_err,3))+"//"+str(round(r_value,3))
# calculatedIRI5 = slope * np.array(array4050) + intercept
# mean_absolute_error5=mean_absolute_error(allDataIRI5, calculatedIRI5)
#
# trace5 = go.Scatter(
#     x=calculatedIRI5,
#     y=allDataIRI5,
#     mode='markers',
#     name=str(round(r_value,3))
# )
# fig1.append_trace(trace5, 1, 5)
#
#
# data = [trace1, trace2, trace3, trace4, trace5]
# # fig1['layout']['xaxis1'].update(title=str(mean_absolute_error1), range=[2, 9])
# fig1['layout']['xaxis2'].update(title=str(mean_absolute_error2), range=[3, 9])
# fig1['layout']['xaxis3'].update(title=str(mean_absolute_error3), range=[4, 9])
# fig1['layout']['xaxis4'].update(title=str(mean_absolute_error4), range=[3, 9])
# fig1['layout']['xaxis5'].update(title=str(mean_absolute_error5), range=[3, 9])
# fig1['layout'].update(height=600, width=1500,)
# plotly.offline.plot(fig1, filename='predictionSpeeds100.html')
#
#
#

print("=================10====================")
# print({
#     "slope":slope,
#     "intercept":intercept,
#     "MAE":mean_absolute_error11
# })
print("================10=20====================")
# print({
#     "slope":slope1,
#     "intercept":intercept1,
#     "MAE":mean_absolute_error1
# })
print("================20=30====================")
print({
    "slope":slope2,
    "intercept":intercept2,
    "MAE":mean_absolute_error2
})
print("===============30=40=====================")
print({
    "slope":slope3,
    "intercept":intercept3,
    "MAE":mean_absolute_error3
})
print("================40=50====================")
print({
    "slope":slope4,
    "intercept":intercept4,
    "MAE":mean_absolute_error4
})
print("================50=====================")
print({
    "slope":slope5,
    "intercept":intercept5,
    "MAE":mean_absolute_error5
})