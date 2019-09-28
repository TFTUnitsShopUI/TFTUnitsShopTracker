#Could use pywin32api
#https://stackoverflow.com/questions/41688871/python-check-if-mouse-clicked
#https://stackoverflow.com/questions/165495/detecting-mouse-clicks-in-windows-using-python/168996

from pynput import mouse
from pynput.mouse import Button
from pynput import keyboard
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

import pyautogui
import time
import math

import findUnits
import unitTracking
import resolutionInfo as res

REFRESH_KEY = ['d']
DELAY = 0.15
SELLING_BACKGROUND_COLOUR = (13, 20, 22)

unitsAvailable = []

def updateUnitsAvailable(myGUISignal):

    global unitsAvailable
    unitsAvailable = findUnits.fingerprintCharacters(res.resolutionClass, DELAY)
    _updateUnitsAvailableGUI(myGUISignal)

def _updateUnitsAvailableGUI(signal):
    GUIMessage = ""
    trackingMessage = ""
    unitNumber = 0
    #Show some sort of on screen uppdate if already have.
    for unitFingerprint in unitsAvailable:
        if unitTracking.notifyCheck(unitFingerprint):
            #Put a symbol on the UI
            GUIMessage += "+"

            #print("             {0}             ".format(unitTracking.getAmount(unitFingerprint)), end="")
        else:
            #hideLabel(myGUISignal, unitNumber)
            #print("             {0}             ".format("0"), end="")
            GUIMessage += "-"

        #Updates for units the user wants to track
        if unitTracking.notifyTracking(unitFingerprint):
            #TODO: Eventually/When we have to track more things make better signals.
            trackingMessage += "Y"
        else:
            trackingMessage += "N"

        unitNumber += 1

    GUIMessage += trackingMessage
    print(GUIMessage)
    signal.emit(GUIMessage)
   #print("")

#For ease of managing signal messages.dd
def showLabel(signal, unitNumber):
    signal.emit("+" + str(unitNumber))


def hideLabel(signal, unitNumber):
    signal.emit("-" + str(unitNumber))

class MonitorMouse(QObject):
    myGUISignal = pyqtSignal(str)
    lastMouseClick = None

    @pyqtSlot()
    def mouseEvents(self):
        with mouse.Listener(
            on_click=self.on_click) as listener:
            listener.join()

    def on_click(self, x, y, button, pressed):

        #LEFT CLICK
        if button == Button.left:
            if pressed:
                #Clicked on Refresh Shop area
                if x > res.resolutionClass.REFRESH_BUTTON[0][0] and x < res.resolutionClass.REFRESH_BUTTON[1][0]:
                    if y > res.resolutionClass.REFRESH_BUTTON[0][1] and y < res.resolutionClass.REFRESH_BUTTON[1][1]:
                        updateUnitsAvailable(self.myGUISignal)

                """Clicking twice, once to pickup, second to sell champions may trigger
                a buy. The UI updates too slowly to read a pixel on/right after a click
                and a delay makes it feel bad to use. To be fixed in the future."""

                #Two ways to use mouse to sell:
                #Click on unit (shop changes UI), click on shop.
                #IF YOU CLICKED ON A UNIT, YOU CANNOT BUY NEXT CLICK.
                if self.lastMouseClick is None:
                    #UI Of shop will change if you clicked on a unit.

                    #This will take time to run and the check below will already go through
                    #if you're buying. Otherwise, the next click will be blocked because
                    #lastMouseClick will have changed.
                    self.myGUISignal.emit("sell")

                #Did not click on a unit, so you can buy.
                if unitsAvailable and self.lastMouseClick is None:
                    numUnitPurchased = findUnits.checkUnitClick(res.resolutionClass, x, y)                

                    if numUnitPurchased is not None and (unitsAvailable[numUnitPurchased] != 0):
                        unitID = unitsAvailable[numUnitPurchased]
                        unitTracking.buyUnit(unitID)
                        unitsAvailable[numUnitPurchased] = 0

                        #Get rid of symbol on GUI after purchase.
                        hideLabel(self.myGUISignal, numUnitPurchased)

                else:
                    #Second click: If you clicked on the shop area. (Probably ish)
                    self.lastMouseClick = None
            #Dragged
            else:
                if self.lastMouseClick is not None:
                    self.lastMouseClick = None

    #RIGHT CLICK
        if pressed and button == Button.right:

            #If right clicked on a unit, which means RESET TRACKING FOR UNIT
            unitClicked = findUnits.checkUnitClick(res.resolutionClass, x, y)
            if unitClicked is not None:
                try:
                    unitTracking.stopTrackingUnit(unitsAvailable[unitClicked])
                    #Modify GUI to instantly show change in tracking.
                    hideLabel(self.myGUISignal, unitClicked)

                except IndexError:
                    #TODO: give user promp to refresh shop manually
                    print("Refresh shop manually")

            #Right clicked not on the shop area. Do something in the future maybe.
            else:
                pass
        if pressed and button == Button.middle:
            unitTracking.reset()
            #Hide labels after reset
            for i in range(0, 5):
                hideLabel(self.myGUISignal, i)


"""Reads Keyboard Inputs (Just D for shop refresh for now)"""
class MonitorKeyboard(QObject):
    myGUISignal = pyqtSignal(str)

    @pyqtSlot()
    def keyPressEvent(self):
        with keyboard.Listener(
            on_press=self.on_press) as listener:
            listener.join()

    def on_press(self, key):
        global unitsAvailable
        try:
            if key.char in REFRESH_KEY:
                updateUnitsAvailable(self.myGUISignal)
        except AttributeError:
            #Key combinations here (space, ctrl c, etc)
            pass


def checkRoundStart(function):
    #pixelRGB = ImageGrab.grab().getpixel((1278, 200))
    global unitsAvailable
    roundTimerX = res.resolutionClass.END_TIMER_PIXEL[0]
    roundTimerY = res.resolutionClass.END_TIMER_PIXEL[1]
    if pyautogui.pixelMatchesColor(roundTimerX, roundTimerY, (233,187,27), tolerance=5):

        unitsAvailable = findUnits.fingerprintCharacters(res.resolutionClass)
        response = ""
        trackingMessage = ""
        for i in range(0, len(unitsAvailable)):
            if unitTracking.notifyCheck(unitsAvailable[i]):
                #Put a symbol on the UI
                response += "+"

                #print("             {0}             ".format(unitTracking.getAmount(unitFingerprint)), end="")
            else:
                #print("             {0}             ".format("0"), end="")
                response += "-"

            #Updates for units the user wants to track
            if unitTracking.notifyTracking(unitsAvailable[i]):
                #TODO: Eventually/When we have to track more things make better signals.
                trackingMessage += "Y"
            else:
                trackingMessage += "N"

        response += trackingMessage

        #Either was doing something on foreground and tabbed in so shorter timer
        #or first round so shorter timer.
        if not pyautogui.pixelMatchesColor(res.resolutionClass.START_TIMER_PIXEL[0],
            res.resolutionClass.START_TIMER_PIXEL[1], (233,187,27), tolerance=5):

            response += "shorter"
        function(response)

    else:
        #Sets a shorter, default timer.
        function(None)

def checkShopColour(mouseMonitor):
    shopMiddle = (math.floor((res.resolutionClass.REFRESH_BUTTON[0][0] + res.resolutionClass.REFRESH_BUTTON[1][0])/2),
        math.floor((res.resolutionClass.REFRESH_BUTTON[0][1] + res.resolutionClass.REFRESH_BUTTON[1][1])/2))
    if pyautogui.pixelMatchesColor(shopMiddle[0], shopMiddle[1], SELLING_BACKGROUND_COLOUR, tolerance=1):
        mouseMonitor.lastMouseClick = "clicked unit"

if __name__ == "__main__":
    # thread = Thread(target = pyQTPractice.run)
    # thread.start()
    # thread.join()
    print('running events')



