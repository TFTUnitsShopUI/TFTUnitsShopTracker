from PyQt5.QtWidgets import QMainWindow, QLabel, QApplication, QPushButton
from PyQt5.QtCore import Qt, QRect, QThread, pyqtSlot, QTimer
from PyQt5.QtGui import QPixmap

import resolutionInfo
import sys
import events
import unitPickerWindow

#IF RUNNING EXECUTABLE
#_basePath = getattr(sys, '_MEIPASS','.')
#PATH_TO_IMAGE = _basePath + ".\\Assets_Stats_Button.png"
#PATH_TO_EXPAND = 

#IF USING COMMAND LINE
PATH_TO_PURCHASED_IMAGE = "Assets_Stats_Button.png"
PATH_TO_TRACKING_IMAGE = "trackingSymbol.png"
PATH_TO_EXPAND = "expand.png"


resolutionClass = resolutionInfo.resolutionClass
timer = None


def hideLabel(label):
    label.hide()

def showLabel(label):
    label.show()


class Overlay(QMainWindow):

    def __init__(self):
        super(Overlay, self).__init__()
        # app = QApplication(sys.argv)
        #window = QMainWindow()
        self.setGeometry(
                    resolutionClass.SHOP_X, resolutionClass.SHOP_Y,
                    resolutionClass.CHAMPION_CARD*resolutionInfo.UNITS_IN_SHOP + sum(resolutionClass.SHOP_SPACING) +55,
                    resolutionClass.SHOP_HEIGHT)

        #window.setAttribute(Qt.WA_NoSystemBackground, True)
        #window.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)

        self.setAttribute(Qt.WA_TranslucentBackground)
        #window.setWindowOpacity(0.1)
        self.compositionWindow = None


        #Green labels to track purchase history
        li1 = QLabel(self)
        li1.setPixmap(QPixmap(PATH_TO_PURCHASED_IMAGE))

        li2 = QLabel(self)
        li2.setPixmap(QPixmap(PATH_TO_PURCHASED_IMAGE))
        li2.setGeometry(QRect(resolutionClass.CHAMPION_CARD + resolutionClass.SHOP_SPACING[1], 0,37,35))

        li3 = QLabel(self)
        li3.setPixmap(QPixmap(PATH_TO_PURCHASED_IMAGE))
        li3.setGeometry(QRect(resolutionClass.CHAMPION_CARD*2 + sum(resolutionClass.SHOP_SPACING[0:3]), 0,37,35))

        li4 = QLabel(self)
        li4.setPixmap(QPixmap(PATH_TO_PURCHASED_IMAGE))
        li4.setGeometry(QRect(resolutionClass.CHAMPION_CARD*3 + sum(resolutionClass.SHOP_SPACING[0:4]), 0,37,35))

        li5 = QLabel(self)
        li5.setPixmap(QPixmap(PATH_TO_PURCHASED_IMAGE))
        li5.setGeometry(QRect(resolutionClass.CHAMPION_CARD*4 + sum(resolutionClass.SHOP_SPACING), 0,37,35))

        self.labels = [li1, li2, li3, li4, li5]

        self.trackingLabels = []
        for i in range(1, resolutionInfo.UNITS_IN_SHOP + 1):
            label = QLabel(self)
            label.setPixmap(QPixmap(PATH_TO_TRACKING_IMAGE))
            label.setGeometry(QRect(resolutionClass.CHAMPION_CARD*i + sum(resolutionClass.SHOP_SPACING[0:i]) - 37, 0,37,35))
            self.trackingLabels.append(label)
   

        #Labels that user decided to manually track

        expandLabel = QLabel(self)
        expandPicture = QPixmap(PATH_TO_EXPAND)
        expandLabel.setPixmap(expandPicture.scaledToHeight(20))
        expandLabel.setGeometry(QRect(resolutionClass.CHAMPION_CARD*5 + sum(resolutionClass.SHOP_SPACING) + 10, 0,55,55))
        expandLabel.mousePressEvent = self.showUnitComposition

        #self.expandButton.setGeometry()

        self.show()


        #Start mouse monitor thread
        self.monitorEvents = events.MonitorMouse()
        self.thread = QThread(self)
        self.monitorEvents.myGUISignal.connect(self.readMouseEvents)
        self.monitorEvents.moveToThread(self.thread)
        self.thread.started.connect(self.monitorEvents.mouseEvents)
        self.thread.start()

        #Start keyboard monitor thread
        self.monitorEventsKey = events.MonitorKeyboard()
        self.threadKey = QThread(self)
        #Sends same signals as mouse press anyway
        self.monitorEventsKey.myGUISignal.connect(self.readMouseEvents)
        self.monitorEventsKey.moveToThread(self.threadKey)
        self.threadKey.started.connect(self.monitorEventsKey.keyPressEvent)
        self.threadKey.start()
        #self.startThread()

    @pyqtSlot(str)
    def readMouseEvents(self, msg):
        if len(msg) == 2:
            if msg[0] == '+':
                self.labels[int(msg[1])].show()
            else:
                self.labels[int(msg[1])].hide()
                self.trackingLabels[int(msg[1])].hide()
                #Remove highlighted options in tracking
                self.compositionWindow = unitPickerWindow.compositionWindow()


        else:
            if msg == "sell":
                checkSelling()
            else:
                #Try sending 1 signal instead of 5
                for i in range(10):
                    #Purchased units
                    if msg[i] == '+':
                        self.labels[i].show()
                    elif msg[i] == '-':
                        self.labels[i].hide()

                    #Chosen to track
                    #TODO: Managing of the message better.
                    elif msg[i] == 'Y':
                        self.trackingLabels[i-resolutionInfo.UNITS_IN_SHOP].show()
                    else:
                        self.trackingLabels[i-resolutionInfo.UNITS_IN_SHOP].hide()
                       


    #Called when the expand button is pressed
    def showUnitComposition(self, event):
        if self.compositionWindow is None:
            self.compositionWindow = unitPickerWindow.compositionWindow()
            self.compositionWindow.show()
        else:
            if self.compositionWindow.isVisible():
                self.compositionWindow.hide()
            else:
                self.compositionWindow.show()


def readStartRoundEvent(msg):
    if msg is None:
        timer.start(900)
    else:
        for i in range(10):
            #Purchased units
            if msg[i] == '+':
                overlay.labels[i].show()
            elif msg[i] == '-':
                overlay.labels[i].hide()

            #Chosen to track
            #TODO: Managing of the message better.
            elif msg[i] == 'Y':
                overlay.trackingLabels[i-resolutionInfo.UNITS_IN_SHOP].show()
            else:
                 overlay.trackingLabels[i-resolutionInfo.UNITS_IN_SHOP].hide()
                   

        if 'shorter' in msg:
            timer.start(20000)
        else:
            timer.start(45000)

def checkSelling():
    QTimer.singleShot(150, (lambda: events.checkShopColour(overlay.monitorEvents)))


# thread = Thread(target=run, daemon=True)
# thread.start()
if __name__ == "__main__":
    app = QApplication(sys.argv)
    overlay = Overlay()

    timer = QTimer()
    timer.timeout.connect(lambda: events.checkRoundStart(readStartRoundEvent))
    timer.start(1000)

    sys.exit(app.exec_())