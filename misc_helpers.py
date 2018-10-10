def decrementCounter(countDict, key, removalVal):
    countDict[key] -= removalVal
    if countDict[key] <= 0:
        del countDict[key]
