import json
import numpy as np
import math

print(math.log10(1))
exit()

def find_nearest_above(my_array, target):
    diff = my_array - target
    mask = np.ma.less_equal(diff, 0)
    # We need to mask the negative differences and zero
    # since we are looking for values above
    if np.all(mask):
        return None  # returns None if target is greater than any value
    masked_diff = np.ma.masked_array(diff, mask)
    return masked_diff.argmin()


acceTreshold = 6
timeSlot = 100

with open('j7ThalallaRandom2.json') as data_file:
    array1 = json.load(data_file)

newArray = {}
timeArray = []
for item in array1:
    newArray[item["time"]] = item
    timeArray.append(item["time"])
    print(item["acceY_raw"])

startTime = array1[0]["time"]
currentTime = startTime
pulseCount = 0
status = True

newDataArray = []
while (status):
    # print(startTime,startTime + timeSlot)
    currentTime = currentTime + timeSlot
    if currentTime >= array1[-1]["time"]:
        status = False
        continue
    nearestLessValue = None
    nearestGreaterValue = None
    for idx, val in enumerate(array1):
        if currentTime >= val["time"]:
            nearestLessValue = val["time"]
        if nearestGreaterValue == None and currentTime < val["time"]:
            nearestGreaterValue = val["time"]

    calcAcceY = newArray[nearestLessValue]["acceY_raw"] + (currentTime - nearestLessValue) * (
                newArray[nearestGreaterValue]["acceY_raw"] - newArray[nearestLessValue]["acceY_raw"]) / (
                            nearestGreaterValue - nearestLessValue)

    if calcAcceY > acceTreshold:
        pulseCount += 1

print(pulseCount)

def pulseCounter(timeSlot, acceTreshold, dataArray):
    newArray = {}
    timeArray = []
    for item in dataArray:
        newArray[item["time"]] = item
        timeArray.append(item["time"])
        # print(item["acceY_raw"])

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
                nearestLessValue = val["time"]
            if nearestGreaterValue == None and currentTime < val["time"]:
                nearestGreaterValue = val["time"]

        calcAcceY = newArray[nearestLessValue]["acceY_raw"] + (currentTime - nearestLessValue) * (
                newArray[nearestGreaterValue]["acceY_raw"] - newArray[nearestLessValue]["acceY_raw"]) / (
                            nearestGreaterValue - nearestLessValue)

        if calcAcceY > acceTreshold:
            pulseCount += 1

    return pulseCount