"""operationalPlanning
@author: cjing9017
@date: 2019/05/13
"""

from PyQt5.QtWidgets import QWidget, QLabel, QLCDNumber
from PyQt5.QtWidgets import QHBoxLayout, QFrame, QPushButton, QVBoxLayout
from PyQt5.QtWidgets import QDesktopWidget, QDialog
from PyQt5.Qt import QIcon, QFont, QSize
from PyQt5.QtCore import Qt, QTimer
from algorithms.AlgorithmExample import AlgorithmAgent
import time, threading
from resource import globalInformation
from util.getQssFile import GetQssFile
from popupWindow.listDialog import ListDialog
from popupWindow.mapDescriptionDialog import MapDescriptionDialog
from resource import strings

from barWindow.frameLessWindow import FramelessWindow
from util.signal import Signal
from common.Config import *
import time
from util.logs import Log
import logging


class OperationalPlanning(QWidget):

    def __init__(self):
        super(OperationalPlanning, self).__init__()
        self.setObjectName('OperationalPlanning')
        self.setStyleSheet(GetQssFile.readQss('../resource/qss/operationalPlanning.qss'))

        self.log = logging.getLogger('StarCraftII')
        # test fix algorithm
        self.algorithm = None
        self.algorithmThread = None

        # font
        font = QFont()
        font.setWeight(50)
        font.setPixelSize(15)

        # set widget of layout
        self.frame = QFrame(self)
        self.frame.setGeometry(QDesktopWidget().screenGeometry())
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setSpacing(20)
        self.setLayout(self.main_layout)

        # start action
        self.start = QPushButton()
        self.start.setObjectName('start')
        self.startLabel = QLabel('start')
        self.startLabel.setFont(font)
        self.start_layout = QVBoxLayout()
        self.start_layout.addWidget(self.start, alignment=Qt.AlignCenter)
        self.start_layout.addWidget(self.startLabel, alignment=Qt.AlignCenter)
        self.main_layout.addLayout(self.start_layout)

        # pause action
        self.pause = QPushButton()
        self.pause.setObjectName('pause')
        self.pauseLabel = QLabel('pause')
        self.pauseLabel.setFont(font)
        self.pause_layout = QVBoxLayout()
        self.pause_layout.addWidget(self.pause, alignment=Qt.AlignCenter)
        self.pause_layout.addWidget(self.pauseLabel, alignment=Qt.AlignCenter)
        self.main_layout.addLayout(self.pause_layout)

        # stop action
        self.stop = QPushButton()
        self.stop.setObjectName('stop')
        self.stopLabel = QLabel('stop')
        self.stopLabel.setFont(font)
        self.stop_layout = QVBoxLayout()
        self.stop_layout.addWidget(self.stop, alignment=Qt.AlignCenter)
        self.stop_layout.addWidget(self.stopLabel, alignment=Qt.AlignCenter)
        self.main_layout.addLayout(self.stop_layout)

        # switch policy action
        self.switch = QPushButton()
        self.switch.setObjectName('switch')
        self.switchLabel = QLabel('switch policy')
        self.switchLabel.setFont(font)
        self.switch_layout = QVBoxLayout()
        self.switch_layout.addWidget(self.switch, alignment=Qt.AlignCenter)
        self.switch_layout.addWidget(self.switchLabel, alignment=Qt.AlignCenter)
        self.main_layout.addLayout(self.switch_layout)

        # simulation time
        self.lcd = QLCDNumber()
        self.lcd.setObjectName('lcd')
        self.lcd.setDigitCount(10)
        self.lcd.setMode(QLCDNumber.Dec)
        self.lcd.setSegmentStyle(QLCDNumber.Flat)
        self.lcd.display(time.strftime("%X", time.localtime()))
        self.lcdLabel = QLabel('simulation time')
        self.lcdLabel.setFont(font)
        self.lcd_layout = QVBoxLayout()
        self.lcd_layout.addWidget(self.lcd, alignment=Qt.AlignCenter)
        self.lcd_layout.addWidget(self.lcdLabel, alignment=Qt.AlignCenter)
        self.main_layout.addLayout(self.lcd_layout)

        # map description
        self.map = QPushButton()
        self.map.setObjectName('map')
        self.mapLabel = QLabel('map description')
        self.mapLabel.setFont(font)
        self.map_layout = QVBoxLayout()
        self.map_layout.addWidget(self.map, alignment=Qt.AlignCenter)
        self.map_layout.addWidget(self.mapLabel, alignment=Qt.AlignCenter)
        self.main_layout.addLayout(self.map_layout)

        # add stretch
        self.main_layout.addStretch(1)

        # popup window
        self.dialog = None

        # initialization
        self.initUI()

    def initUI(self):
        # connect the slot function
        self.start.clicked.connect(self.buttonEvent)
        self.pause.clicked.connect(self.buttonEvent)
        self.stop.clicked.connect(self.buttonEvent)
        self.switch.clicked.connect(self.buttonEvent)
        self.map.clicked.connect(self.buttonEvent)

    def buttonEvent(self):
        sender = self.sender()
        if sender == self.start:
            self.startEvent()
        elif sender == self.pause:
            self.pauseEvent()
        elif sender == self.stop:
            self.stopEvent()
        elif sender == self.switch:
            self.switchEvent()
        elif sender == self.map:
            self.mapEvent()

    # start simulation
    def startEvent(self):
        message = 'start the simulation'
        self.log.info(message)
        Signal.get_signal().emit_signal(message)
        # fix rl algorithm
        self.algorithm = AlgorithmAgent()
        self.algorithmThread = threading.Thread(
            target=self.algorithm.algorithm(globalInformation.get_value('current_map_name')),
            name='StarCraft2Thread')

    # pause simulation
    def pauseEvent(self):
        message = 'pause the simulation'
        self.log.info(message)
        Signal.get_signal().emit_signal(message)

    # stop simulation
    def stopEvent(self):
        message = 'stop the simulation'
        self.log.info(message)
        Signal.get_signal().emit_signal(message)

    # a description of current map
    def mapEvent(self):
        message = 'open the map description'
        self.log.info(message)
        Signal.get_signal().emit_signal(message)
        self.window = FramelessWindow('map description')
        self.dialog = QDialog()
        mapDialog = MapDescriptionDialog()
        mapDialog.setupUi(self.dialog)
        self.dialog.setModal(True)
        self.window.setWidget(self.dialog)
        self.initFrameLessWindow(
            QSize(700, 600),
            'Operational Planning',
            QIcon('../resource/drawable/logo.png')
        )
        self.window.show()
        # self.dialog.show()

    # switch policy of a dialog
    # there is a description of each algorithm
    def switchEvent(self):
        message = 'switch policy'
        self.log.info(message)
        Signal.get_signal().emit_signal(message)
        self.window = FramelessWindow('switch policy')
        self.dialog = QDialog()
        # tab item name
        list_str = [strings.ALGORITHM1, strings.ALGORITHM2, strings.ALGORITHM3]
        # item content
        list_item = [strings.CLASS_ALGORITHM1, strings.CLASS_ALGORITHM2, strings.CLASS_ALGORITHM3]
        # title name
        self.listDialog = ListDialog(list_str, list_item, strings.OPERATIONAL_PLANNING_TITLE, strings.TYPE_POLICY)
        self.listDialog.setupUi(self.dialog, self.window)
        self.window.setWidget(self.dialog)
        self.initFrameLessWindow(
            QSize(700, 600),
            'Operational Planning',
            QIcon('../resource/drawable/logo.png')
        )
        self.window.show()
        # self.dialog.setModal(True)
        # self.dialog.show()

    def initFrameLessWindow(self, size, title, icon):
        self.window.resize(size)
        self.window.setWindowTitle(title)
        self.window.setWindowIcon(icon)
