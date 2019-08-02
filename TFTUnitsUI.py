from PyQt5.QtWidgets import QMainWindow, QLabel, QApplication
from PyQt5.QtCore import Qt, QRect, QThread, pyqtSlot, QTimer
from PyQt5.QtGui import QPixmap

import resolutionInfo
import sys
import events

#IF RUNNING EXECUTABLE
_basePath = getattr(sys, '_MEIPASS','.')
PATH_TO_IMAGE = _basePath + ".\\Assets_Stats_Button.png"

#IF USING COMMAND LINE
#PATH_TO_IMAGE = "Assets_Stats_Button.png"

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
                    resolutionClass.CHAMPION_CARD*resolutionInfo.UNITS_IN_SHOP + sum(resolutionClass.SHOP_SPACING),
                    resolutionClass.SHOP_HEIGHT)

        #window.setAttribute(Qt.WA_NoSystemBackground, True)
        #window.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)

        self.setAttribute(Qt.WA_TranslucentBackground)
        #window.setWindowOpacity(0.1)


        li1 = QLabel(self)
        li1.setPixmap(QPixmap(PATH_TO_IMAGE))

        li2 = QLabel(self)
        li2.setPixmap(QPixmap(PATH_TO_IMAGE))
        li2.setGeometry(QRect(resolutionClass.CHAMPION_CARD + resolutionClass.SHOP_SPACING[1], 0,37,35))

        li3 = QLabel(self)
        li3.setPixmap(QPixmap(PATH_TO_IMAGE))
        li3.setGeometry(QRect(resolutionClass.CHAMPION_CARD*2 + sum(resolutionClass.SHOP_SPACING[0:3]), 0,37,35))

        li4 = QLabel(self)
        li4.setPixmap(QPixmap(PATH_TO_IMAGE))
        li4.setGeometry(QRect(resolutionClass.CHAMPION_CARD*3 + sum(resolutionClass.SHOP_SPACING[0:4]), 0,37,35))

        li5 = QLabel(self)
        li5.setPixmap(QPixmap(PATH_TO_IMAGE))
        li5.setGeometry(QRect(resolutionClass.CHAMPION_CARD*4 + sum(resolutionClass.SHOP_SPACING), 0,37,35))

        self.labels = [li1, li2, li3, li4, li5]
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
        else:
            if msg == "sell":
                checkSelling()
            else:
                #Try sending 1 signal instead of 5
                for i in range(len(msg)):
                    if msg[i] == '+':
                        self.labels[i].show()
                    else:
                        self.labels[i].hide()


def readStartRoundEvent(msg):
    if msg is None:
        timer.start(900)
    else:
        #Try sending 1 signal instead of 5
        for i in range(resolutionInfo.UNITS_IN_SHOP):
            if msg[i] == '+':
                overlay.labels[i].show()
            else:
                overlay.labels[i].hide()

        if len(msg) > resolutionInfo.UNITS_IN_SHOP:
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

    #Run some other python code
    timer = QTimer()
    timer.timeout.connect(lambda: events.checkRoundStart(readStartRoundEvent))
    timer.start(1000)

    sys.exit(app.exec_())