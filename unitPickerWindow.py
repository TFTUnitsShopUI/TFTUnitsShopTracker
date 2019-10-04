from PyQt5.QtCore import Qt, QThread
from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout, QToolTip
from PyQt5.QtGui import QPixmap, QPainter, QCursor
from PyQt5 import QtWidgets
import resolutionInfo
import unitTracking

""" Originally designed so nonoe of the GUI files HAVE to interact with the back
end besides events.py which is meant as the inbetween. As a result this goes through
TFTUnitsUI.py -> events.py -> unitTracking.py
"""

opacity = 0.4
trackUnits = []

#Returns (name of champion, Pixmap of picture)
def getChampionsAsPixmap(path="championList.txt"):
    pixmaps = []
    with open(path, 'r') as file:
        for name in file:
            strippedName = name.strip('\n')
            champPixMap = QPixmap("champion\\" + strippedName + ".png")
            pixmaps.append((strippedName, champPixMap.scaledToHeight(50)))
    return pixmaps

def getTransparentPixmap(pixmap):
    output = QPixmap(pixmap.size())
    output.fill(Qt.transparent)
    transparencyFilter = QPainter(output)
    transparencyFilter.setOpacity(opacity)
    transparencyFilter.drawPixmap(0,0,pixmap)
    transparencyFilter.end()
    return output



""" Each label's mousePressEvent can only take 1 argument (event) which would return
a QMouseEvent from a click. This method is called and is used to REPLACE the function
passed to label.mousePressEvent.

This is done to be able to store the information we
need to later update/display the label correctly.

Usage:  mouseEvent = bindLabelInfo(*Info to be passed*)
        label.mousePressEvent = mouseEvent
instead of just:
        label.mousePressEvent = clickedUnitList
"""
def bindLabelInfo(name, origPixmap, label):
    return lambda event: _clickedUnitList(event, name, origPixmap, label)

def _clickedUnitList(event, name, origPixmap, label):
    print(name)
    pixmap = label.pixmap()

    #Has been selected
    if pixmap.hasAlpha():
        label.setPixmap(origPixmap)

        #SEND SIGNAL TO EVENTS
        unitTracking.startTracking(name)

    else:
        label.setPixmap(getTransparentPixmap(origPixmap))
        unitTracking.stopTracking(name)

def bindHoverName(name, label):
    return lambda event: _hoverEvent(event, name, label)

def _hoverEvent(event, name, label):
    #label.setToolTip(name)
    QToolTip.showText(QCursor.pos(), name)

class compositionWindow(QMainWindow):
    def __init__(self):
        super(compositionWindow, self).__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        #self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        #self.setWindowOpacity(opacity)


        self.pixmaps = getChampionsAsPixmap()

        self.widget = QtWidgets.QWidget(self)
        self.layout = QGridLayout()
        self.widget.setLayout(self.layout)
        #self.widget.setStyleSheet('QMainWindow{background-color: darkgray;}')
        self.widget.setStyleSheet("background-image: url(background.png)")
        self.setCentralWidget(self.widget)

        for row in range(7):
            for column in range(9):
                champNumber = row*9 + column
                if champNumber < len(self.pixmaps):
                    label = QLabel(self)

                    #Start everything 'unclicked' i.e. transparent'ish
                    label.setPixmap(getTransparentPixmap(self.pixmaps[champNumber][1]))
                    #Change appearance depending on selected
                    mouseEvent = bindLabelInfo(self.pixmaps[champNumber][0], self.pixmaps[champNumber][1], label)
                    hoverEvent = bindHoverName(self.pixmaps[champNumber][0], label)
                    label.setMouseTracking(True)
                    label.mousePressEvent = mouseEvent
                    label.mouseMoveEvent = hoverEvent
                    self.layout.addWidget(label, row, column)


        xCoord = resolutionInfo.resolutionClass.CHAMPION_CARD*resolutionInfo.UNITS_IN_SHOP + sum(
            resolutionInfo.resolutionClass.SHOP_SPACING) + resolutionInfo.resolutionClass.SHOP_X - self.frameGeometry().width()/2
        yCoord = resolutionInfo.resolutionClass.SHOP_Y - self.frameGeometry().height()

        self.move(xCoord, yCoord)
