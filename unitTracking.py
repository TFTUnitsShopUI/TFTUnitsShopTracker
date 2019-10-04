import mouseEvents
import time
import sys
import ast

unitsBought = {}
unitsToTrack = []

fingerprintToName = {}

with open("championFingerprint.txt", 'r') as file:
    for line in file:
        if ':' in line:
            value, key = [text.strip('\n') for text in line.split(" : ")]
            
            #Convert from string (that are valid tuples written to file) to a tuple
            fingerprintToName[tuple(ast.literal_eval(key))] = value


"""Marks the figerprint as bought."""
def buyUnit(unitID):
    if unitID not in unitsBought:
        unitsBought[unitID] = 1
    else:
        unitsBought[unitID] = unitsBought[unitID] + 1

def startTracking(name):
    print("Start tracking " + name)
    unitsToTrack.append(name)

def stopTracking(name):
    if name in unitsToTrack:
        unitsToTrack.remove(name)

def stopTrackingUnit(unitID):
    if unitID in unitsBought:
        unitsBought.pop(unitID)
    # if unitID in fingerprintToName:
    #     if fingerprintToName[unitID] in unitsToTrack:
    #         unitsToTrack.remove(fingerprintToName[unitID])


def notifyCheck(unitFingerprint):
    return unitFingerprint in unitsBought

def notifyTracking(unitFingerprint):
    if unitFingerprint in fingerprintToName:
        return fingerprintToName[unitFingerprint] in unitsToTrack
    else:
        print("List of units OUTDATED, update of unit list is required\n", file=sys.stderr)

def getAmount(unitFingerprint):
    return unitsBought[unitFingerprint]

def reset():
    unitsBought.clear()
    unitsToTrack.clear()


if __name__ == "__main__":
    pass
                



