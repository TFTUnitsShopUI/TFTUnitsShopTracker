from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout
from PyQt5.QtGui import QPixmap
from PyQt5 import QtWidgets
import resolutionInfo

def getChampionsAsPixmap(path="championList.txt"):
    pixmaps = []
    with open(path, 'r') as file:
        for name in file:
            champPixMap = QPixmap("championPictures\\" + name.strip('\n') + "_0.jpg")
            pixmaps.append(champPixMap.scaledToHeight(50))
    return pixmaps


class compositionWindow(QMainWindow):
    def __init__(self):
        super(compositionWindow, self).__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)

        self.pixmaps = getChampionsAsPixmap()

        self.widget = QtWidgets.QWidget(self)
        self.layout = QGridLayout()
        self.widget.setLayout(self.layout)
        self.widget.setStyleSheet('QMainWindow{background-color: darkgray;}')
        self.setCentralWidget(self.widget)


        xCoord = resolutionInfo.resolutionClass.CHAMPION_CARD*resolutionInfo.UNITS_IN_SHOP + sum(resolutionInfo.resolutionClass.SHOP_SPACING) + resolutionInfo.resolutionClass.SHOP_X - self.frameGeometry().width()/2,
        yCoord = resolutionInfo.resolutionClass.SHOP_Y - resolutionInfo.resolutionClass.SHOP_HEIGHT

        for row in range(7):
            for column in range(9):
                champNumber = row*9 + column
                if champNumber < len(self.pixmaps):
                    label = QLabel(self)
                    label.setPixmap(self.pixmaps[champNumber])
                    self.layout.addWidget(label, row, column)
        self.move(0, 1238)

