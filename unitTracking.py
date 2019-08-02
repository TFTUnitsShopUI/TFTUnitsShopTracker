import mouseEvents
import time


unitsBought = {}

"""Marks the figerprint as bought."""
def buyUnit(unitID):
    if unitID not in unitsBought:
        unitsBought[unitID] = 1
    else:
        unitsBought[unitID] = unitsBought[unitID] + 1

def stopTrackingUnit(unitID):
    if unitID in unitsBought:
        unitsBought.pop(unitID)

def notifyCheck(unitFingerprint):
    return unitFingerprint in unitsBought

def getAmount(unitFingerprint):
    return unitsBought[unitFingerprint]

def reset():
    unitsBought.clear()


if __name__ == "__main__":

    with mouseEvents.mouse.Listener(
        on_click=mouseEvents.on_click) as listener:
        listener.join()


