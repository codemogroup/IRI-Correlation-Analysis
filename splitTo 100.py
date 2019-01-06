import json
import math
import xlrd
from plotly import tools
import plotly.plotly
import plotly.graph_objs as go
import numpy as np
import glob
import math

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

def newPulseCounter(acceTresholdY, acceTresholdX, acceTresholdZ, dataArray):
    pulseCountY = 0
    pulseCountX = 0
    pulseCountZ = 0
    for data1 in dataArray:
        acceY = abs(data1["acceY"] - 9.8)
        acceX = abs(data1["acceX"])*10**10
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


array1 =None
with open("iroadsData/gallefaceToKollupitiya.json") as data_file:
    array1 = json.load(data_file)

print(str(array1[0]["lat"]) + "," + str(array1[0]["lon"]))
print(str(array1[-1]["lat"]) + "," + str(array1[-1]["lon"]))

distanceArray = []
totalDistance = 0
for idx, item in enumerate(array1):
    if idx > 0:
        distance = getDistance(array1[idx]["lon"], array1[idx]["lat"], array1[idx-1]["lon"], array1[idx-1]["lat"])
        if distance > 0:
            totalDistance = totalDistance + distance
            distanceArray.append({"distance": distance,
                                  "index": idx})
            print({"distance": distance, "index": idx})

splittedData = []

# for item in distanceArray:


print(totalDistance)