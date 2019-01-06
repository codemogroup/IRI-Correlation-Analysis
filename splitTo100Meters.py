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

perMeter = 1

allgpsData = []
xforGPS = []
xcount = 0

thresholdValue = 0.08
acceTresholdX = 1.2
acceTresholdY = 0.15
acceTresholdZ = 0.05

def getSpeedBand(speed):

    if speed < 10:
        return 1
    elif speed < 20:
        return 2
    elif speed < 30:
        return 3
    elif speed < 40:
        return 4
    elif speed < 50:
        return 5
    else:
        return 6


def newPulseCounter(acceTresholdY, acceTresholdX, acceTresholdZ, dataArray):
    pulseCountY = 0
    pulseCountX = 0
    pulseCountZ = 0
    for data1 in dataArray:
        acceY = abs(data1["acceY"] - 9.8)
        acceX = abs(data1["acceX_raw"])
        acceZ = abs(data1["acceZ"])
        # print(acceX)
        if acceY > acceTresholdY:
            pulseCountY = pulseCountY + 1
        if acceX > acceTresholdX:
            pulseCountX = pulseCountX + 1
        if acceZ > acceTresholdZ:
            pulseCountZ = pulseCountZ + 1

    return {
            "pulseCountY": pulseCountY,
            "pulseCountX": pulseCountX,
            "pulseCountZ": pulseCountZ
            }


def pulseCounter(timeSlot, acceTreshold, dataArray):
    arrayY = []
    for data1 in dataArray:
        acceY = data1["acceY"] - 9.8
        if acceY < 0:
            acceY = acceY * -1
        arrayY.append(acceY)

    newAcceData = []
    newTimeData = []
    newArray = {}
    timeArray = []
    for item in dataArray:
        newArray[item["time"]] = item
        timeArray.append(item["time"])
        # print(item["acceY_raw"])
    # print(dataArray)
    startTime = dataArray[0]["time"]
    currentTime = startTime
    pulseCount = 0
    status = True

    newDataArray = []
    while (status):
        # print(startTime,startTime + timeSlot)
        currentTime = currentTime + timeSlot
        if currentTime >= dataArray[-1]["time"]:
            status = False
            continue
        nearestLessValue = None
        nearestGreaterValue = None
        for idx, val in enumerate(dataArray):
            if currentTime >= val["time"]:
                nearestLessValue = idx
            if nearestGreaterValue == None and currentTime < val["time"]:
                nearestGreaterValue = idx

        calcAcceY = arrayY[nearestLessValue] + (currentTime - dataArray[nearestLessValue]["time"]) * (
                arrayY[nearestGreaterValue] - arrayY[nearestLessValue]) / (
                dataArray[nearestGreaterValue]["time"] - dataArray[nearestLessValue]["time"])
        # print(calcAcceY)
        newAcceData.append(calcAcceY)
        newTimeData.append(currentTime - startTime)
        if calcAcceY > acceTreshold:

            pulseCount += 1
    # print(newTimeData)
    return {
            "newTimeData": newTimeData,
            "newAcceData": newAcceData,
            "pulseCount": pulseCount
            }

def getDistance(lon1, lat1, lon2, lat2):
    # print()
    r = 6371000
    phi1 = getRadiant(lat1)
    phi2 = getRadiant(lat2)
    deltaPhi = getRadiant(lat2 - lat1)
    deltaLamda = getRadiant(lon2 - lon1)
    a = math.sin(deltaPhi / 2.0) * math.sin(deltaPhi / 2.0) + math.cos(phi1) * math.cos(phi2) * math.sin(deltaLamda / 2.0) * math.sin(deltaLamda / 2.0)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    meters = r * c
    km = meters / 1000.0
    # print(lon1, lat1, lon2, lat2, km)
    return km


def getRadiant(degree):
    radiant = degree * (2 * math.pi / 360)
    return radiant


romdasDataExcelFiles = glob.glob("romdasData/*.xlsx")
fig = tools.make_subplots(rows=11, cols=1)
fig['layout'].update(height=4500, width=1200, title='Actual vs Calculated Pulse count')
dataGraphs = []
dataSDGraphs = []
dataSMeanGraphs = []
logDataGraphs = []
IRIDataGraphs = []
spikesGraphs = []
figcount = 0

allDataActualSpikes = []
allDataCalcSpikesAll = []
allDataCalcSpikesY = []
allDataCalcSpikesX = []
allDataCalcSpikesZ = []
# allDataCalcSpikesAll = []
allDataLogActualSpikes = []
allDataLogCalcSpikes = []
allDataIRI = []

alldataSpeed = []
alldataSpeedTest = []
allGPSdataSpeed = []
allGPSdataSpeed1 = []
allGPSdataSpeed1Test = []
speedBandsR = []
speedBandsI = []

accesYMAXValue = []
accesXMAXValue = []
accesZMAXValue = []

accesYMeanValues = []
accesYSDValues = []


accesXMeanValues = []
accesXSDValues = []

accesZMeanValues = []
accesZSDValues = []

spikesActualLog = []
spikesCalcLog = []

for file in romdasDataExcelFiles:
    figcount = figcount + 1
    print(figcount)
    fileName = file.replace("romdasData\\", "").replace(".xlsx", "")
    iroadsFilepath = "iroadsData\\" + fileName + ".json"

    # exit()
    array1 =None
    with open(iroadsFilepath) as data_file:
        array1 = json.load(data_file)
    coordinate = None
    for idx, item in enumerate(array1):
        # print(item["lat"], item["lon"])

        if idx == 0:
            coordinate = str(item["lat"]) + "/" + str(item["lon"])
            item["gpsStatus"] = "C"
        else:
            if coordinate == str(item["lat"]) + "/" + str(item["lon"]):
                item["gpsStatus"] = "U"
            else:
                item["gpsStatus"] = "C"
                coordinate = str(item["lat"]) + "/" + str(item["lon"])
    lastChangedIdx = 0

    # print(array1[0]["lat"])
    # print(array1[0]["lon"])
    #
    # print(array1[-1]["lat"])
    # print(array1[-1]["lon"])
    #

    #
    # print(getDistance(array1[0]["lon"], array1[0]["lat"], array1[-1]["lon"], array1[-1]["lat"]))

    totalDistance = 0
    count = 0
    lastItem = array1[0]
    timeCount = 0
    array1[0]["timeN"] = 0
    for idx, item in enumerate(array1):
        if idx != 0:
            timeCount = timeCount + (array1[idx]["time"] - array1[idx-1]["time"])/1000
            item["timeN"] = timeCount
            # print(timeCount)
        # print(item["gpsStatus"], "====", item["lat"], ",", item["lon"])
        if item["gpsStatus"] == "C" and idx != 0:
            count = count + 1
            if count > 4:
                # print(item["lat"] , item["lon"])
                # print(array1[idx-1]["lat"] , array1[idx-1]["lon"])
                totalDistance = totalDistance + getDistance(array1[idx]["lon"], array1[idx]["lat"], lastItem["lon"], lastItem["lat"])
                # print(totalDistance)¿
                count = 0
                lastItem =item
        # if item["gpsStatus"] == "C" and idx!=lastChangedIdx:
        #     print(getDistance(array1[idx]["lon"], array1[idx]["lat"],array1[lastChangedIdx]["lon"], array1[lastChangedIdx]["lat"])*3600000/(array1[idx]["time"]-array1[lastChangedIdx]["time"]))
        #     lastChangedIdx = idx
        #
        #
        #
        # if idx != len(array1)-1:
        #     print(item["lat"])
        #     print(getDistance(array1[idx+1]["lon"], array1[idx+1]["lat"],array1[idx]["lon"], array1[idx]["lat"])*3600000/(array1[idx+1]["time"]-array1[idx]["time"]))


    # print(totalDistance)¿

    iriData = []
    loc = ("romdasData\\" + fileName + ".xlsx")
    # To open Workbook
    wb = xlrd.open_workbook(loc)
    sheet = wb.sheet_by_index(0)
    noOfRows = sheet.nrows

    for i in range(1, noOfRows-perMeter+1,perMeter):
        dataRow = {}
        dataRow["chainage"] = sheet.cell_value(i+perMeter-1, 0)
        speed1 = 0
        for j in range(0, perMeter):
            speed1 = speed1 + sheet.cell_value(i+j, 1)/perMeter
        dataRow["speed"] = speed1
        rough1 = 0
        for j in range(0,perMeter):
            rough1 = rough1 + sheet.cell_value(i+j, 3)
        dataRow["rough1"] = rough1
        dataRow["time"] = sheet.cell_value(i+perMeter-1, 5)
        iri1 = 0
        for j in range(0, perMeter):
            iri1 = iri1 + sheet.cell_value(i+j, 7)/perMeter
        dataRow["iri"] = iri1
        iriData.append(dataRow)

    # print(iriData)
    print(((array1[-1]["time"] - array1[0]["time"])) / 1000)
    print(iriData[-1]["time"])
    print(fileName)

    for idx1, item1 in enumerate(iriData):
        newDataForStep = []
        for idx2, item2 in enumerate(array1):

            # if idx1 == 0:
            #     if item2["timeN"] <= item1["time"]:
            #         newDataForStep.append(item2)

            # if idx1 != 0 or idx1 != len(iriData) - 1:
            if item2["timeN"] <= item1["time"] and item2["timeN"] > iriData[idx1 -1]["time"]:
                newDataForStep.append(item2)

        if len(newDataForStep) == 0:
            iriData = iriData[0:len(iriData) - 1]
        else:
            item1["data1"] = newDataForStep

    # for idx1, item1 in enumerate(iriData):
    #     if idx1 != 0:
    #         print(len(item1["data1"]) , item1["time"] - iriData[idx1 -1]["time"])

    dataPulse = None

    spikesActual = []
    spikesCalc = []
    # accesYMeanValues = []
    # accesYSDValues = []
    iri = []
    iriData = iriData[1:len(iriData)]
    for step in iriData:
        # if dataPulse["pulseCount"] < 250:
        gpsDistance = []
        accesYValues = []
        accesXValues = []
        accesZValues = []
        gpsSpeed = []
        distance = getDistance(step["data1"][0]["lon"], step["data1"][0]["lat"], step["data1"][-1]["lon"], step["data1"][-1]["lat"])
        # print(distance*1000)
        time = (step["data1"][-1]["time"] - step["data1"][0]["time"])/3600000
        # print(distance/time,step["speed"])
        allgpsData.append(distance/time)
        for idx, item in enumerate(step["data1"]):
            if idx >0:
                distance1 = getDistance(step["data1"][idx- 1]["lon"], step["data1"][idx - 1]["lat"], step["data1"][idx]["lon"],
                                   step["data1"][idx]["lat"])
                gpsDistance.append(distance1)


            # print(item["gpsSpeed"])
            if item["gpsSpeed"] < 100:
                gpsSpeed.append(item["gpsSpeed"])
            accesYValues.append(abs(item["acceY"]-9.8))
            accesXValues.append(abs(item["acceX_raw"]))
            accesZValues.append(abs(item["acceZ"]))
        # print(sum(gpsDistance)/time , distance/time,step["speed"] )
        accesYMAXValue.append(np.max(np.array(accesYValues)))
        accesXMAXValue.append(np.max(np.array(accesXValues)))
        accesZMAXValue.append(np.max(np.array(accesZValues)))
        speedBandsI.append(getSpeedBand(sum(gpsDistance)/time))
        speedBandsR.append(getSpeedBand(step["speed"]))
        allGPSdataSpeed1.append(sum(gpsDistance)/time)
        allGPSdataSpeed.append(np.mean(np.array(gpsSpeed)))
        ystdVal = np.std(np.array(accesYValues))
        yMeanVal = np.mean(np.array(accesYValues))
        xstdVal = np.std(np.array(accesXValues))
        xMeanVal = np.mean(np.array(accesXValues))
        zstdVal = np.std(np.array(accesZValues))
        zMeanVal = np.mean(np.array(accesZValues))
        # dataPulse = pulseCounter(100, thresholdValue, step["data1"])
        dataPulse = newPulseCounter(acceTresholdY, acceTresholdX, acceTresholdZ, step["data1"])

        accesYSDValues.append(ystdVal)
        accesYMeanValues.append(yMeanVal)
        accesXSDValues.append(xstdVal)
        accesXMeanValues.append(xMeanVal)
        accesZSDValues.append(zstdVal)
        accesZMeanValues.append(zMeanVal)

        spikesActual.append(step["rough1"])
        spikesCalc.append(dataPulse["pulseCountY"])
        iri.append(step["iri"])
        allDataActualSpikes.append(step["rough1"])
        allDataCalcSpikesAll.append(dataPulse["pulseCountY"] + dataPulse["pulseCountX"] )
        allDataCalcSpikesY.append(dataPulse["pulseCountY"])
        allDataCalcSpikesX.append(dataPulse["pulseCountX"])
        allDataCalcSpikesZ.append(dataPulse["pulseCountZ"])
        # allDataCalcSpikesAll.append(dataPulse["pulseCountY"]  )
        allDataIRI.append(step["iri"])
        alldataSpeed.append(step["speed"])


    spikesActualLog = []
    spikesCalcLog = []

    for dataPoint in spikesCalc:
        if dataPoint == 0:
            spikesCalcLog.append(0)
            allDataLogCalcSpikes.append(0)
        else:
            spikesCalcLog.append(math.log10(dataPoint))
            allDataLogCalcSpikes.append(math.log10(dataPoint))
    for dataPoint in spikesActual:
        if dataPoint == 0:
            spikesActualLog.append(0)
            allDataLogActualSpikes.append(0)
        else:
            spikesActualLog.append(math.log10(dataPoint))
            allDataLogActualSpikes.append(math.log10(dataPoint))

    arrayX = []
    arrayY = []



    # for data1 in iriData[0]["data1"]:
        # arrayX.append(data1["timeN"])
        # arrayY = dataPulse["newAcceData"]
        # arrayX = dataPulse["newTimeData"]
        # acceY = data1["acceY"] -9.8
        # if acceY < 0:
        #     acceY = acceY*-1
        #
        #
        # arrayY.append(acceY)

#     trace1 = go.Scatter(
#         x=spikesActual,
#         y=spikesCalc,
#         mode='markers',
#         name=fileName
#     )
#     dataGraphs.append(trace1)
#     fig.append_trace(trace1, figcount, 1)
#
#
#     trace2 = go.Scatter(
#         x=spikesActual,
#         y=accesYSDValues,
#         mode='markers',
#         name=fileName
#     )
#     dataSDGraphs.append(trace2)
#
#     trace3 = go.Scatter(
#         x=spikesActual,
#         y=accesYMeanValues,
#         mode='markers',
#         name=fileName
#     )
#     dataSMeanGraphs.append(trace3)
#
#     traceLog = go.Scatter(
#         x=spikesActualLog,
#         y=spikesCalcLog,
#         mode='markers',
#         name=fileName
#     )
#     logDataGraphs.append(traceLog)
#
#     traceIRI = go.Scatter(
#         x=iri,
#         y=spikesCalc,
#         mode='markers',
#         name=" Calc Y"
#     )
#     IRIDataGraphs.append(traceIRI)
#
#
# corReCOEFFY = np.corrcoef(allDataActualSpikes, allDataCalcSpikesY)[0][1]
# corReCOEFFX = np.corrcoef(allDataActualSpikes, allDataCalcSpikesX)[0][1]
# corReCOEFFZ = np.corrcoef(allDataActualSpikes, allDataCalcSpikesZ)[0][1]
# corReCOEFFAll = np.corrcoef(allDataActualSpikes, allDataCalcSpikesAll)[0][1]
#
# traceAllY = go.Scatter(
#         x=allDataActualSpikes,
#         y=allDataCalcSpikesY,
#         mode='markers',
#         name=" Calc Y = " + str(corReCOEFFY)
# )
# spikesGraphs.append(traceAllY)
#
# traceAllX = go.Scatter(
#         x=allDataActualSpikes,
#         y=allDataCalcSpikesX,
#         mode='markers',
#         name="Calc X = " + str(corReCOEFFX)
# )
# spikesGraphs.append(traceAllX)
#
# traceAllZ = go.Scatter(
#         x=allDataActualSpikes,
#         y=allDataCalcSpikesZ,
#         mode='markers',
#         name="Calc Z = " + str(corReCOEFFZ)
# )
# spikesGraphs.append(traceAllZ)
#
# traceAll = go.Scatter(
#         x=allDataCalcSpikesX,
#         y=allDataActualSpikes,
#         mode='markers',
#         name="gpsSpeed = "
#     )
# spikesGraphs.append(traceAll)
#
# corel = str(np.corrcoef(allDataCalcSpikesX, allDataActualSpikes)[0][1])
#
# plotly.offline.plot({
#         "data": spikesGraphs,
#         "layout": go.Layout(title="Ac vs CAL All " + corel )
# }, auto_open=True, filename='ac vs cal x+y.html')
# #
# print("CorRel == ", np.corrcoef(allDataActualSpikes, allDataCalcSpikesX)[0][1])
# print("CorRel == ", np.corrcoef(alldataSpeed, allgpsData)[0][1])

# plotly.offline.plot(fig, filename='graphs.html')

# corReCOEFF = np.corrcoef(allDataActualSpikes, allDataCalcSpikesY)[0][1]
#
# plotly.offline.plot({
#         "data": dataGraphs,
#         "layout": go.Layout(title="Romdas Spikes VS Iroads Spikes  Threshold = " + str(thresholdValue) + " CORCOEFF = " + str(corReCOEFF))
# }, auto_open=True, filename='all Threshold = ' + str(thresholdValue) + '.html')
#
# corReCOEFF = np.corrcoef(allDataLogActualSpikes, allDataLogCalcSpikes)[0][1]
# plotly.offline.plot({
#         "data": logDataGraphs,
#         "layout": go.Layout(title="Log(Romdas Spikes) VS Log(Iroads Spikes) Threshold = " + str(thresholdValue) + " CORCOEFF = " + str(corReCOEFF))
# }, auto_open=True, filename='log Threshold = ' + str(thresholdValue) + '.html')
#
# corReCOEFF = np.corrcoef(allDataIRI, allDataCalcSpikesY)[0][1]
# plotly.offline.plot({
#         "data": IRIDataGraphs,
#         "layout": go.Layout(title="IRI VS Iroads Spikes Threshold = " + str(thresholdValue) + " CORCOEFF = " + str(corReCOEFF))
# }, auto_open=True, filename='IRI Threshold = ' + str(thresholdValue) + '.html')

# plotly.offline.plot({
#         "data": dataSDGraphs,
#         "layout": go.Layout(title="Romdas Spikes VS acceY STD Value")
# }, auto_open=True, filename='sd.html')
#
# plotly.offline.plot({
#         "data": dataSMeanGraphs,
#         "layout": go.Layout(title="Romdas Spikes VS acceY Mean Value")
# }, auto_open=True, filename='mean.html')

# print(((array1[-1]["time"] - array1[0]["time"]))/1000)
# print(iriData[-1]["time"])

import csv
with open('iridata'+str(perMeter)+'00T.csv', mode='w', encoding='utf-8') as csv_file1:
    fieldnames = ['romdasSpikes', "calcSpikesY", "calcSpikesX", "calcSpikesZ","calcSpikesAll", "iri" ,"meanY", "sdY", "meanX", "sdX", "meanZ", "sdZ", "romLog", "iroadLog", "speed", "gpsSpeed","yMax", "xMax", "zMax"]
    writer = csv.DictWriter(csv_file1, fieldnames=fieldnames)
    writer.writeheader()

    for idx,val in enumerate(allDataActualSpikes):
        writer.writerow({
            'romdasSpikes': val,
            "calcSpikesY": allDataCalcSpikesY[idx],
            "calcSpikesX": allDataCalcSpikesX[idx],
            "calcSpikesZ": allDataCalcSpikesZ[idx],
            "iri": allDataIRI[idx],
            "meanY": accesYMeanValues[idx],
            "sdY": accesYSDValues[idx],
            "meanX": accesXMeanValues[idx],
            "sdX": accesXSDValues[idx],
            "meanZ": accesZMeanValues[idx],
            "sdZ": accesZSDValues[idx],
            "romLog": allDataLogActualSpikes[idx],
            "iroadLog": allDataLogCalcSpikes[idx],
            "speed": alldataSpeed[idx],
            "gpsSpeed": allGPSdataSpeed1[idx],
            "calcSpikesAll":allDataCalcSpikesAll[idx],
            "yMax": accesYMAXValue[idx],
            "xMax": accesXMAXValue[idx],
            "zMax": accesZMAXValue[idx]
        })

# Polynomial = np.polynomial.Polynomial
#
# # The data: conc = [P] and absorbance, A
# conc = np.array(allDataIRI)
# A = np.array(allDataCalcSpikesY)
#
# cmin, cmax = min(conc), max(conc)
# pfit, stats = Polynomial.fit(conc, A, 1, full=True, window=(cmin, cmax),domain=(cmin, cmax))
#
# print('Raw fit results:', pfit, stats, sep='\n')
#
# A0, m = pfit
# resid, rank, sing_val, rcond = stats
# rms = np.sqrt(resid[0]/len(A))
#
# print('Fit: A = {:.3f}[P] + {:.3f}'.format(m, A0),
#       '(rms residual = {:.4f})'.format(rms))
#
# pylab.plot(conc, A, 'o', color='k')
# pylab.plot(conc, pfit(conc), color='k')
# pylab.xlabel('Romdas')
# pylab.ylabel('Iroads')
# pylab.show()

#////////////////////////////////////////////////////////////////////
# newIRIarray= []
#
#
allDataIRI = np.array(allDataIRI)
allDataCalcSpikesY = np.array(allDataCalcSpikesY)
#
slope, intercept, r_value, p_value, std_err = stats.linregress(allDataCalcSpikesY, allDataIRI)
slopeX, interceptX, r_valueX, p_valueX, std_errX = stats.linregress(allDataCalcSpikesX, allDataIRI)



#
# title = "y="+ str(round(slope,5)) + "x+" + str(round(intercept,5)) + "///" + str(round(std_err,5))+"//"+str(round(r_value, 5))
# print("===============================")
# print(title)
# print("===============================")
# data123 = {
#     "slope":slope,
#     "intercept":intercept,
#     "r_value":r_value,
#     "p_value":p_value,
#     "std_err":std_err
# }
# line = slope * allDataCalcSpikesY + intercept
#
# # Creating the dataset, and generating the plot
# trace1 = go.Scatter(
#     x=allDataCalcSpikesY,
#     y=allDataIRI,
#     mode='markers',
#     marker=go.Marker(color='rgb(255, 127, 14)'),
#     name='Data'
# )
#
# trace2 = go.Scatter(
#     x=allDataCalcSpikesY,
#     y=line,
#     mode='lines',
#     marker=go.Marker(color='rgb(31, 119, 180)'),
#     name='Fit'
# )
#
# # annotation = go.Annotation(
# #     x=3.5,
# #     y=23.5,
# #     text='$R^2 = 0.9551,\\Y = 0.716X + 19.18$',
# #     showarrow=False,
# #     font=go.Font(size=16)
# # )
# layout = go.Layout(
#     title=title,
#     height=600,
#     width=600,
#
# )
#
# data = [trace1, trace2]
# fig = go.Figure(data=data, layout=layout)
# fig['layout']['xaxis'].update(range=[0, 250])
# fig['layout']['yaxis'].update(range=[0, 9])
# plotly.offline.plot(fig, filename='bestfit-500.html')
#
# testride = "parlimentRoadToPannipitiya"
#
# iroadsFilepath = "iroadsData\\" + testride + ".json"
# romdasFilepath = "romdasData\\" + testride + ".xlsx"
# array1 = None
# with open(iroadsFilepath) as data_file:
#     array1 = json.load(data_file)
# timeCount = 0
# array1[0]["timeN"] = 0
# for idx, item in enumerate(array1):
#     if idx != 0:
#         timeCount = timeCount + (array1[idx]["time"] - array1[idx-1]["time"])/1000
#         item["timeN"] = timeCount
# iriData = []
# loc = romdasFilepath
# # To open Workbook
# wb = xlrd.open_workbook(loc)
# sheet = wb.sheet_by_index(0)
# noOfRows = sheet.nrows
#
# for i in range(1, noOfRows - perMeter + 1, perMeter):
#     dataRow = {}
#     dataRow["chainage"] = sheet.cell_value(i + perMeter - 1, 0)
#     speed1 = 0
#     for j in range(0, perMeter):
#         speed1 = speed1 + sheet.cell_value(i + j, 1) / perMeter
#     dataRow["speed"] = speed1
#     rough1 = 0
#     for j in range(0, perMeter):
#         rough1 = rough1 + sheet.cell_value(i + j, 3)
#     dataRow["rough1"] = rough1
#     dataRow["time"] = sheet.cell_value(i + perMeter - 1, 5)
#     iri1 = 0
#     for j in range(0, perMeter):
#         iri1 = iri1 + sheet.cell_value(i + j, 7) / perMeter
#     dataRow["iri"] = iri1
#     iriData.append(dataRow)
#
# for idx1, item1 in enumerate(iriData):
#     newDataForStep = []
#     for idx2, item2 in enumerate(array1):
#         if item2["timeN"] <= item1["time"] and item2["timeN"] > iriData[idx1 -1]["time"]:
#             newDataForStep.append(item2)
#
#
#     item1["data1"] = newDataForStep
#
# iriData = iriData[1:len(iriData)]
#
# actualIRI = []
# spikesCalc1 = []
# for step in iriData:
#     dataPulse = newPulseCounter(acceTresholdY, acceTresholdX, acceTresholdZ, step["data1"])
#     actualIRI.append(step["iri"])
#     spikesCalc1.append(dataPulse["pulseCountY"])
#
# calculatedIRI = slope * np.array(allDataCalcSpikesY) + intercept
#
# trace1234 = go.Scatter(
#     x=calculatedIRI,
#     y=allDataIRI,
#     mode='markers',
#     name='Data'
# )
# mean_absolute_error=mean_absolute_error(allDataIRI, calculatedIRI)
# print("mean_squared_error")
# print(mean_squared_error(allDataIRI, calculatedIRI))
# layout = go.Layout(
#     title=str(mean_absolute_error),
#     height=600,
#     width=600
# )
# data = [trace1234]
# fig = go.Figure(data=data, layout=layout)
# plotly.offline.plot(fig, filename='prediction500.html')

romdasDataExcelFilesTEST = glob.glob("romdasData/forCalc/*.xlsx")
allDataCalcSpikesYTest = []
allDataCalcSpikesXTest = []
allDataIRITest = []

for file in ["kasbawaToPolgasowita",
             "bypassRoadToKesbawa",
             "wewalaToBoralasgamuwa",
             "pannipitiyaToKottawa",
          ]:
    # for file in ["uwinHiranaCampus", "uwinKesbawaBandaragama", "dayanaKesbawaBandaragama", "dayanaPiliyandalaKesbewa"]:
    fileName = file
    # fileName = file.replace("romdasData\\forCalc\\", "").replace(".xlsx", "")
    iroadsFilepathTEST = "iroadsData\\" + fileName + ".json"
    print(iroadsFilepathTEST)

    # exit()
    array1TEST = None
    with open(iroadsFilepathTEST) as data_file:
        array1TEST = json.load(data_file)
    coordinate = None
    for idx, item in enumerate(array1TEST):
        # print(item["lat"], item["lon"])

        if idx == 0:
            coordinate = str(item["lat"]) + "/" + str(item["lon"])
            item["gpsStatus"] = "C"
        else:
            if coordinate == str(item["lat"]) + "/" + str(item["lon"]):
                item["gpsStatus"] = "U"
            else:
                item["gpsStatus"] = "C"
                coordinate = str(item["lat"]) + "/" + str(item["lon"])
    lastChangedIdx = 0

    totalDistance = 0
    count = 0
    lastItem = array1TEST[0]
    timeCount = 0
    array1TEST[0]["timeN"] = 0
    for idx, item in enumerate(array1TEST):
        if idx != 0:
            timeCount = timeCount + (array1TEST[idx]["time"] - array1TEST[idx - 1]["time"]) / 1000
            item["timeN"] = timeCount
            # print(timeCount)
        # print(item["gpsStatus"], "====", item["lat"], ",", item["lon"])
        if item["gpsStatus"] == "C" and idx != 0:
            count = count + 1
            if count > 4:
                # print(item["lat"] , item["lon"])
                # print(array1[idx-1]["lat"] , array1[idx-1]["lon"])
                totalDistance = totalDistance + getDistance(array1TEST[idx]["lon"], array1TEST[idx]["lat"],
                                                            lastItem["lon"], lastItem["lat"])
                # print(totalDistance)¿
                count = 0
                lastItem = item

    iriData = []
    loc = ("romdasData\\forCalc\\" + fileName + ".xlsx")
    # To open Workbook
    wb = xlrd.open_workbook(loc)
    sheet = wb.sheet_by_index(0)
    noOfRows = sheet.nrows

    for i in range(1, noOfRows - perMeter + 1, perMeter):
        dataRow = {}
        dataRow["chainage"] = sheet.cell_value(i + perMeter - 1, 0)
        speed1 = 0
        for j in range(0, perMeter):
            speed1 = speed1 + sheet.cell_value(i + j, 1) / perMeter
        dataRow["speed"] = speed1
        rough1 = 0
        for j in range(0, perMeter):
            rough1 = rough1 + sheet.cell_value(i + j, 3)
        dataRow["rough1"] = rough1
        dataRow["time"] = sheet.cell_value(i + perMeter - 1, 5)
        iri1 = 0
        for j in range(0, perMeter):
            iri1 = iri1 + sheet.cell_value(i + j, 7) / perMeter
        dataRow["iri"] = iri1
        iriData.append(dataRow)

    # print(iriData)
    print(((array1TEST[-1]["time"] - array1TEST[0]["time"])) / 1000)
    print(iriData[-1]["time"])
    print(fileName)

    for idx1, item1 in enumerate(iriData):
        newDataForStep = []
        for idx2, item2 in enumerate(array1TEST):

            # if idx1 == 0:
            #     if item2["timeN"] <= item1["time"]:
            #         newDataForStep.append(item2)

            # if idx1 != 0 or idx1 != len(iriData) - 1:
            if item2["timeN"] <= item1["time"] and item2["timeN"] > iriData[idx1 - 1]["time"]:
                newDataForStep.append(item2)

        if len(newDataForStep) == 0:
            iriData = iriData[0:len(iriData) - 1]
        else:
            item1["data1"] = newDataForStep

    # for idx1, item1 in enumerate(iriData):
    #     if idx1 != 0:
    #         print(len(item1["data1"]) , item1["time"] - iriData[idx1 -1]["time"])

    dataPulse = None

    spikesActual = []
    spikesCalc = []
    # accesYMeanValues = []
    # accesYSDValues = []
    iri = []
    iriData = iriData[1:len(iriData)]
    for step in iriData:
        # if dataPulse["pulseCount"] < 250:
        gpsDistance = []
        accesYValues = []
        accesXValues = []
        accesZValues = []
        gpsSpeed = []
        distance = getDistance(step["data1"][0]["lon"], step["data1"][0]["lat"], step["data1"][-1]["lon"],
                               step["data1"][-1]["lat"])
        # print(distance*1000)
        time = (step["data1"][-1]["time"] - step["data1"][0]["time"]) / 3600000
        # print(distance/time,step["speed"])
        allgpsData.append(distance / time)
        for idx, item in enumerate(step["data1"]):
            if idx > 0:
                distance1 = getDistance(step["data1"][idx - 1]["lon"], step["data1"][idx - 1]["lat"],
                                        step["data1"][idx]["lon"],
                                        step["data1"][idx]["lat"])
                gpsDistance.append(distance1)

            # print(item["gpsSpeed"])
            if item["gpsSpeed"] < 100:
                gpsSpeed.append(item["gpsSpeed"])
            accesYValues.append(abs(item["acceY"] - 9.8))
            accesXValues.append(abs(item["acceX_raw"]))
            accesZValues.append(abs(item["acceZ"]))
        # print(sum(gpsDistance)/time , distance/time,step["speed"] )

        # dataPulse = pulseCounter(100, thresholdValue, step["data1"])
        dataPulse = newPulseCounter(acceTresholdY, acceTresholdX, acceTresholdZ, step["data1"])
        allDataCalcSpikesYTest.append(dataPulse["pulseCountY"])
        allDataCalcSpikesXTest.append(dataPulse["pulseCountX"])
        # allDataCalcSpikesAll.append(dataPulse["pulseCountY"]  )
        allDataIRITest.append(step["iri"])
        alldataSpeedTest.append(step["speed"])
        allGPSdataSpeed1Test.append(sum(gpsDistance) / time)



calculatedIRI12 = slope * np.array(allDataCalcSpikesYTest) + intercept
mean_absolute_error123=mean_absolute_error(np.array(allDataIRITest), calculatedIRI12)
print("mean_absolute_error123",mean_absolute_error123)
calculatedIRI12X = slopeX * np.array(allDataCalcSpikesXTest) + interceptX
mean_absolute_error123X=mean_absolute_error(np.array(allDataIRITest), calculatedIRI12X)

dictActual = {}
dictCalc = {}
dictCalcX = {}

for idx,item in enumerate(allDataIRITest):
    dictActual[str(idx)] = item
    dictCalc[str(idx)] = calculatedIRI12[idx]
    dictCalcX[str(idx)] = calculatedIRI12X[idx]
import operator
sorted_x = sorted(dictActual.items(), key=operator.itemgetter(1))
newIRIAc = []
newIRICAlc = []
newIRICAlcX = []
newIRICAlcXY = []
print(sorted_x)
for key in sorted_x:
    newIRIAc.append(dictActual[key[0]])
    newIRICAlc.append(dictCalc[key[0]])
    newIRICAlcX.append(dictCalcX[key[0]])
    newIRICAlcXY.append((dictCalcX[key[0]] + dictCalc[key[0]])/2.0)

mean_absolute_error123Xy=mean_absolute_error(np.array(newIRIAc), np.array(newIRICAlcXY))

print("mean_absolute_error :",mean_absolute_error123)

count123 = []
for idx,i in enumerate(allDataIRITest):
    count123.append(idx+1)
spikesGraphs = []
traceActual = go.Scatter(
        x=count123,
        y=newIRIAc,
        mode='lines',
        name="Actual"
    )
traceCalc = go.Scatter(
        x=count123,
        y=newIRICAlc,
        mode='markers',
        name="Calculated : " + str(round(mean_absolute_error123,5))
    )

traceCalcX = go.Scatter(
        x=count123,
        y=newIRICAlcX,
        mode='markers',
        name="Calculated X : " + str(round(mean_absolute_error123X,5))
    )

traceCalcXY = go.Scatter(
        x=count123,
        y=newIRICAlcXY,
        mode='markers',
        name="Calculated XY : " + str(round(mean_absolute_error123Xy,5))
    )
trace22 = go.Scatter(
        x=newIRIAc,
        y=newIRICAlc,
        mode='markers',
        name="Calculated"
    )
spikesGraphs.append(traceActual)
spikesGraphs.append(traceCalc)
spikesGraphs.append(traceCalcX)
spikesGraphs.append(traceCalcXY)

fig11 = tools.make_subplots(rows=1, cols=1)
fig11.add_trace(trace22,1,1)
fig11['layout']['xaxis'].update(range=[2,10])
fig11['layout']['yaxis'].update(range=[2,10])

fig11['layout'].update(height=600, width=600,)
plotly.offline.plot(fig11, filename='g123g500.html')

plotly.offline.plot({
        "data": spikesGraphs,
        "layout": go.Layout(yaxis=dict(range=[2,10]),title="Ac vs CAL All 500:"+str(round(mean_absolute_error123,5)))
}, auto_open=True, filename='actualVSPredictedIRI300.html')

with open('iridata'+str(perMeter)+'00P.csv', mode='w', encoding='utf-8') as csv_file1:
    fieldnames = ['romdasSpikes', "calcSpikesY", "calcSpikesX", "calcSpikesZ","calcSpikesAll", "iri" ,"meanY", "sdY", "meanX", "sdX", "meanZ", "sdZ", "romLog", "iroadLog", "speed", "gpsSpeed","yMax", "xMax", "zMax"]
    writer = csv.DictWriter(csv_file1, fieldnames=fieldnames)
    writer.writeheader()

    for idx,val in enumerate(allDataIRITest):
        writer.writerow({
            'romdasSpikes': "",
            "calcSpikesY": allDataCalcSpikesYTest[idx],
            "calcSpikesX": allDataCalcSpikesXTest[idx],
            "calcSpikesZ": "",
            "iri": allDataIRITest[idx],
            "meanY": "",
            "sdY": "",
            "meanX": "",
            "sdX": "",
            "meanZ": "",
            "sdZ": "",
            "romLog":"",
            "iroadLog": "",
            "speed": alldataSpeedTest[idx],
            "gpsSpeed": allGPSdataSpeed1Test[idx],
            "calcSpikesAll":"",
            "yMax": "",
            "xMax": "",
            "zMax": ""
        })

spikesGraphs123 = []
traceActual = go.Scatter(
        x=alldataSpeedTest,
        y=allGPSdataSpeed1Test,
        mode='markers',
        name="Actual"
    )

spikesGraphs123.append(traceActual)
plotly.offline.plot({
        "data": spikesGraphs123,
        "layout": go.Layout(title="Ac vs CAL All1234 :",xaxis=dict(range=[0,50]),yaxis=dict(range=[0,50]))
}, auto_open=True, filename='actualVSPredictedIRI300speed.html')





