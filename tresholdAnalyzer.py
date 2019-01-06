import json
import math
import xlrd
from plotly import tools
import plotly.plotly
import plotly.graph_objs as go
import numpy as np
import glob
import math

perMeter = 5

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
    # print(pulseCountZ)
    return {
            "newTimeData": [],
            "newAcceData": [],
            "pulseCountY": pulseCountY,
            "pulseCountX": pulseCountX,
            "pulseCountZ": pulseCountZ
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


coreArray = []
thresholdArray = []
dataGraphs = []
for i in range(0, 100, 4):
    print("============")
    print(i)
    print("============")
    thresholdValue = i/100
    thresholdArray.append(thresholdValue)
    romdasDataExcelFiles = glob.glob("romdasData/*.xlsx")
    # fig = tools.make_subplots(rows=11, cols=1)
    # fig['layout'].update(height=4500, width=1200, title='Actual vs Calculated Pulse count')

    dataSDGraphs = []
    dataSMeanGraphs = []
    logDataGraphs = []
    IRIDataGraphs = []
    figcount = 0

    allDataActualSpikes = []
    allDataCalcSpikes = []
    allDataLogActualSpikes = []
    allDataLogCalcSpikes = []
    allDataIRI = []

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
        # print(figcount)
        fileName = file.replace("romdasData\\", "").replace(".xlsx", "")
        iroadsFilepath = "iroadsData\\" + fileName + ".json"

        # exit()
        array1 = None
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
                timeCount = timeCount + (array1[idx]["time"] - array1[idx - 1]["time"]) / 1000
                item["timeN"] = timeCount
                # print(timeCount)
            # print(item["gpsStatus"], "====", item["lat"], ",", item["lon"])
            if item["gpsStatus"] == "C" and idx != 0:
                count = count + 1
                if count > 4:
                    # print(item["lat"] , item["lon"])
                    # print(array1[idx-1]["lat"] , array1[idx-1]["lon"])
                    totalDistance = totalDistance + getDistance(array1[idx]["lon"], array1[idx]["lat"], lastItem["lon"],
                                                                lastItem["lat"])
                    # print(totalDistance)¿
                    count = 0
                    lastItem = item
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

        # for i in range(1, noOfRows):
        #     dataRow = {}
        #     dataRow["chainage"] = sheet.cell_value(i, 0)
        #     dataRow["speed"] = sheet.cell_value(i, 1)
        #     dataRow["rough1"] = sheet.cell_value(i, 3)
        #     dataRow["time"] = sheet.cell_value(i, 5)
        #     dataRow["iri"] = sheet.cell_value(i, 7)
        #     iriData.append(dataRow)
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
        # print(((array1[-1]["time"] - array1[0]["time"])) / 1000)
        # print(iriData[-1]["time"])
        print(fileName)

        for idx1, item1 in enumerate(iriData):
            newDataForStep = []
            for idx2, item2 in enumerate(array1):

                if idx1 == 0:
                    if item2["timeN"] <= item1["time"]:
                        newDataForStep.append(item2)

                else:
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

        for step in iriData:
            # dataPulse = pulseCounter(100, thresholdValue, step["data1"])
            dataPulse = newPulseCounter(0.16, 1.2, thresholdValue, step["data1"])

            # if dataPulse["pulseCount"] < 250:
            accesYValues = []
            accesXValues = []
            accesZValues = []
            for item in step["data1"]:
                accesYValues.append(item["acceY"])
                accesXValues.append(item["acceX_raw"])
                accesZValues.append(item["acceZ"])
            ystdVal = np.std(np.array(accesYValues))
            accesYSDValues.append(ystdVal)
            accesYMeanValues.append(np.mean(np.array(accesYValues)))

            accesXSDValues.append(np.std(np.array(accesXValues)))
            accesXMeanValues.append(np.mean(np.array(accesXValues)))

            accesZSDValues.append(np.std(np.array(accesZValues)))
            accesZMeanValues.append(np.mean(np.array(accesZValues)))

            spikesActual.append(step["rough1"])
            spikesCalc.append(dataPulse["pulseCountY"])
            iri.append(step["iri"])
            allDataActualSpikes.append(step["rough1"])
            allDataCalcSpikes.append(dataPulse["pulseCountZ"])
            allDataIRI.append(step["iri"])

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

    corReCOEFF = np.corrcoef(allDataActualSpikes, allDataCalcSpikes)[0][1]
    coreArray.append(corReCOEFF)


trace1 = go.Scatter(
    x=thresholdArray,
    y=coreArray,
    mode='markers',
    name="corRel"
)
dataGraphs.append(trace1)

plotly.offline.plot({
        "data": dataGraphs,
        "layout": go.Layout(title="", height=600, width=600, xaxis=dict(
        title='Accelerometer Threshold(m/s-2)',
        titlefont=dict(
            family='Courier New, monospace',
            size=18,
            color='#7f7f7f'
        )
    ),
    yaxis=dict(
        title='Correlation Coefficient',
        titlefont=dict(
            family='Courier New, monospace',
            size=18,
            color='#7f7f7f'
        )))
}, auto_open=True, filename='correl VS Threshold Z 500.html')