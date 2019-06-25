"""entry function
@author: cjing9017
@date: 2019/05/13
"""
import ctypes
import sys

from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QApplication, QSystemTrayIcon
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QSplitter
from PyQt5.Qt import QIcon, QFont, QSize
from PyQt5.QtWidgets import QDesktopWidget, QListWidget, QStackedWidget
from PyQt5.QtWidgets import QListWidgetItem, QTextEdit
from PyQt5.QtCore import Qt

from view.fight import FightView
from PyQt5.QtCore import Qt
# import stackwidget
from view.pattern import Pattern
from view.operationalPlanning import OperationalPlanning
from view.maps import Maps
from view.replay import Replay
from view.situationInformation import SituationInformation
from view.modelTrain import ModelTrain

from util.getQssFile import GetQssFile
from resource import strings
from resource import globalInformation

from barWindow.frameLessWindow import FramelessWindow


class MainWindow(QWidget):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setObjectName('MainWindow')

        # set attributes of window
        # self.setMinimumSize(1200, 700)
        self.center()
        self.setStyleSheet(GetQssFile.readQss('../resource/qss/menu.qss'))
        # self.setWindowIcon(QIcon())

        # fight visualization
        self.fightview = None
        self.list_widget = None
        self.list_items = None

        # set main layout
        self.main_layout = QVBoxLayout(self, spacing=0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        # set top layout:
        self.top_layout = QVBoxLayout()
        self.main_layout.addLayout(self.top_layout)
        self.setTopLayout()
        # set line
        self.line = QSplitter(Qt.Horizontal)
        self.line.setHandleWidth(10)
        self.main_layout.addWidget(self.line)
        # set bottom layout
        self.bottom_layout = QHBoxLayout()
        self.main_layout.addLayout(self.bottom_layout)
        self.setBottomLayout()
        # the stretch of top layout and bottom layout
        self.main_layout.setStretchFactor(self.top_layout, 1)
        self.main_layout.setStretchFactor(self.bottom_layout, 15)

        # initialize of global information
        globalInformation.init()

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        geometry = self.geometry()
        self.move((screen.width() - geometry.width()) / 2,
                  (screen.height() - geometry.height()) / 2)

    def setTopLayout(self):
        # list menu
        self.list_widget = QListWidget()
        self.list_widget.setMinimumHeight(25)
        self.list_widget.setFlow(QListWidget.LeftToRight)
        self.list_widget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.list_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.list_widget.setFrameShape(QListWidget.NoFrame)
        # list item for menu
        self.list_items = QStackedWidget()

        self.top_layout.addWidget(self.list_widget)
        self.top_layout.addWidget(self.list_items)
        self.top_layout.setStretchFactor(self.list_widget, 1)
        self.top_layout.setStretchFactor(self.list_items, 3)

        self.list_widget.currentRowChanged.connect(
            self.list_items.setCurrentIndex)
        list_str = [
            strings.PATTERN,
            strings.OPERATIONAL_PLANNING,
            strings.MAPS,
            strings.REPLAY,
            strings.SITUATION_INFORMATION,
            strings.MODEL_TRAIN]
        item_view = [
            strings.CLASS_PATTERN,
            strings.CLASS_OPERATIONAL_PLANNING,
            strings.CLASS_MAPS,
            strings.CLASS_REPLAY,
            strings.CLASS_SITUATION_INFORMATION,
            strings.CLASS_MODEL_TRAIN]
        for i in range(len(list_str)):
            font = QFont()
            font.setBold(True)
            font.setWeight(50)
            font.setPixelSize(17)
            # add item to menu
            item = QListWidgetItem(list_str[i], self.list_widget)
            item.setFont(font)
            item.setTextAlignment(Qt.AlignCenter)
            if i == 0:
                item.setSelected(True)
            self.list_items.addWidget(eval(item_view[i]))

    def setBottomLayout(self):
        self.fightview = FightView()
        self.bottom_layout.addWidget(self.fightview)


def main():
    app = QApplication(sys.argv)
    main_window = FramelessWindow()
    main_window.setWindowTitle(strings.NAME)
    main_window.setWindowIcon(QIcon('../resource/drawable/icon.png'))
    main_window.resize(QSize(1200, 700))
    main_window.setWidget(MainWindow())
    main_window.showMaximized()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
