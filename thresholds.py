import json
import math
import xlrd
from plotly import tools
import plotly.plotly
import plotly.graph_objs as go
import numpy as np
import glob




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
    return meters


def getRadiant(degree):
    radiant = degree * (2 * math.pi / 360)
    return radiant


romdasDataExcelFiles = glob.glob("romdasData/*.xlsx")
fig = tools.make_subplots(rows=100, cols=1)
fig['layout'].update(height=1000, width=1200, title='Actual vs Calculated Pulse count')
# dataGraphs = []
dataSDGraphs = []
dataSMeanGraphs = []
figcount = 0
for thresholdVal in range(1, 11):
    dataGraphs = []
    figcount = figcount + 1
    for file in romdasDataExcelFiles:
        # figcount = figcount + 1
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

        for i in range(1, noOfRows):
            dataRow = {}
            dataRow["chainage"] = sheet.cell_value(i, 0)
            dataRow["speed"] = sheet.cell_value(i, 1)
            dataRow["rough1"] = sheet.cell_value(i, 3)
            dataRow["time"] = sheet.cell_value(i, 5)
            dataRow["iri"] = sheet.cell_value(i, 7)
            iriData.append(dataRow)

        # print(iriData)
        # print(((array1[-1]["time"] - array1[0]["time"])) / 1000)
        # print(iriData[-1]["time"])
        # print(fileName)

        for idx1, item1 in enumerate(iriData):
            newDataForStep = []
            for idx2, item2 in enumerate(array1):

                if idx1 == 0:
                    if item2["timeN"] <= item1["time"]:
                        newDataForStep.append(item2)

                else:
                    if item2["timeN"] <= item1["time"] and item2["timeN"] > iriData[idx1 -1]["time"]:
                        newDataForStep.append(item2)

            if len(newDataForStep) == 0:
                iriData = iriData[0:len(iriData)- 1]
            else:
                item1["data1"] = newDataForStep

        # for idx1, item1 in enumerate(iriData):
        #     if idx1 != 0:
        #         print(len(item1["data1"]) , item1["time"] - iriData[idx1 -1]["time"])

        dataPulse = None

        spikesActual = []
        spikesCalc = []
        accesYMeanValues = []
        accesYSDValues = []

        for step in iriData:
            accesYValues = []
            for item in step["data1"]:
                accesYValues.append(item["acceY_raw"])
            accesYSDValues.append(np.std(np.array(accesYValues)))
            accesYMeanValues.append(np.mean(np.array(accesYValues)))
            dataPulse = pulseCounter(100, thresholdVal/100, step["data1"])
            spikesActual.append(step["rough1"])
            spikesCalc.append(dataPulse["pulseCount"])


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

        trace1 = go.Scatter(
            x=spikesActual,
            y=spikesCalc,
            mode='markers',
            name=fileName
        )
        # dataGraphs.append(trace1)
        fig.append_trace(trace1, figcount, 1)


        # trace2 = go.Scatter(
        #     x=spikesActual,
        #     y=accesYSDValues,
        #     mode='markers',
        #     name=fileName
        # )
        # dataSDGraphs.append(trace2)
        #
        # trace3 = go.Scatter(
        #     x=spikesActual,
        #     y=accesYMeanValues,
        #     mode='markers',
        #     name=fileName
        # )
        # dataSMeanGraphs.append(trace3)

    print(figcount)


plotly.offline.plot(fig, filename='graphs.html')

    # plotly.offline.plot({
    #         "data": dataGraphs,
    #         "layout": go.Layout(title="all")
    # }, auto_open=True, filename='all.html')
    #
    # plotly.offline.plot({
    #         "data": dataSDGraphs,
    #         "layout": go.Layout(title="sd")
    # }, auto_open=True, filename='sd.html')
    #
    # plotly.offline.plot({
    #         "data": dataSMeanGraphs,
    #         "layout": go.Layout(title="mean")
    # }, auto_open=True, filename='mean.html')

    # print(((array1[-1]["time"] - array1[0]["time"]))/1000)
    # print(iriData[-1]["time"])