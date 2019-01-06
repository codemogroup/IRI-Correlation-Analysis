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

perMeter = 5

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

romdasDataExcelFilesTEST = glob.glob("romdasData/forCalc/*.xlsx")
allDataCalcSpikesYTest = []
allDataIRITest = []

for file in romdasDataExcelFilesTEST:
    fileName = file.replace("romdasData\\forCalc\\", "").replace(".xlsx", "")
    iroadsFilepathTEST = "iroadsData\\" + fileName + ".json"

    # exit()
    array1TEST =None
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
            timeCount = timeCount + (array1TEST[idx]["time"] - array1TEST[idx-1]["time"])/1000
            item["timeN"] = timeCount
            # print(timeCount)
        # print(item["gpsStatus"], "====", item["lat"], ",", item["lon"])
        if item["gpsStatus"] == "C" and idx != 0:
            count = count + 1
            if count > 4:
                # print(item["lat"] , item["lon"])
                # print(array1[idx-1]["lat"] , array1[idx-1]["lon"])
                totalDistance = totalDistance + getDistance(array1TEST[idx]["lon"], array1TEST[idx]["lat"], lastItem["lon"], lastItem["lat"])
                # print(totalDistance)¿
                count = 0
                lastItem =item

    iriData = []
    loc = ("romdasData\\forCalc\\" + fileName + ".xlsx")
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



        # dataPulse = pulseCounter(100, thresholdValue, step["data1"])
        dataPulse = newPulseCounter(acceTresholdY, acceTresholdX, acceTresholdZ, step["data1"])
        allDataCalcSpikesYTest.append(dataPulse["pulseCountY"])
        # allDataCalcSpikesAll.append(dataPulse["pulseCountY"]  )
        allDataIRITest.append(step["iri"])

