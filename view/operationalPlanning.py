"""operationalPlanning
@author: cjing9017
@date: 2019/05/13
"""

from PyQt5.QtWidgets import QWidget, QLabel, QLCDNumber
from PyQt5.QtWidgets import QHBoxLayout, QFrame, QPushButton, QVBoxLayout
from PyQt5.QtWidgets import QDesktopWidget, QDialog
from PyQt5.Qt import QIcon, QFont, QSize
from PyQt5.QtCore import Qt, QTimer
# from algorithms.AlgorithmExample import AlgorithmAgent
from algorithms.Algorithm import AlgorithmAgent
from algorithms.marl import MARL
import threading
from resource import globalInformation
from util.getQssFile import GetQssFile
from popupWindow.listDialog import ListDialog
from popupWindow.mapDescriptionDialog import MapDescriptionDialog
from resource import strings

from barWindow.frameLessWindow import FramelessWindow
from util.signal import Signal

# from common.Config import *
import time
import logging
import subprocess
import os

from util.timeWorker import TimeWorker

from model.master.masterAgent import MasterAgent


class OperationalPlanning(QWidget):

    signal_gameover = Signal.get_signal().signal_gameover

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
        # self.pause = QPushButton()
        # self.pause.setObjectName('pause')
        # self.pauseLabel = QLabel('pause')
        # self.pauseLabel.setFont(font)
        # self.pause_layout = QVBoxLayout()
        # self.pause_layout.addWidget(self.pause, alignment=Qt.AlignCenter)
        # self.pause_layout.addWidget(self.pauseLabel, alignment=Qt.AlignCenter)
        # self.main_layout.addLayout(self.pause_layout)

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
        self.lcd.setFrameStyle(QFrame.Panel | QFrame.Raised)
        self.lcd.display(time.strftime("%X", time.localtime()))
        self.lcdLabel = QLabel('simulation time')
        self.lcdLabel.setFont(font)
        self.lcd_layout = QVBoxLayout()
        self.lcd_layout.addWidget(self.lcd, alignment=Qt.AlignBottom)
        self.lcd_layout.addWidget(self.lcdLabel, alignment=Qt.AlignBottom)
        self.main_layout.addLayout(self.lcd_layout)

        # define time
        self.qtime = QTimer()
        self.qtime.timeout.connect(self.refresh)

        # define global variable
        global interval
        interval = 0
        global start_or_pause
        start_or_pause = False
        global stop
        stop = True

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

    def refresh(self):
        timeworker = TimeWorker(self.lcd, OperationalPlanning.interval)
        OperationalPlanning.interval += 1
        timeworker.run()

    def initUI(self):
        # connect the slot function
        self.start.clicked.connect(self.buttonEvent)
        # self.pause.clicked.connect(self.buttonEvent)
        self.stop.clicked.connect(self.buttonEvent)
        self.switch.clicked.connect(self.buttonEvent)
        self.map.clicked.connect(self.buttonEvent)
        self.signal_gameover.connect(self.stopEvent)

    def buttonEvent(self):
        sender = self.sender()
        if sender == self.start:
            self.startEvent()
        # elif sender == self.pause:
        #     self.pauseEvent()
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
        Signal.get_signal().emit_signal_str(message)
        # fix rl algorithm

        globalInformation.set_value(strings.IS_STOP, False)

        OperationalPlanning.interval = 0
        OperationalPlanning.start_or_pause = True
        OperationalPlanning.stop = False
        self.qtime.start(1000)

        def playWithHuman():
            subprocess.Popen(strings.PLAY_WITH_HUMAN)

        def playWithMachine():
            """
                map_name = '3m'
                difficulty = '3'

                param_set = {}
                param_set['gamma'] = 0.99
                param_set['td_lambda'] = 0.8
                param_set['learning_rate'] = 0.0005
                param_set['alpha'] = 0.99
                param_set['eps'] = 1e-05
                param_set['epsilon_start'] = 1
                param_set['epsilon_end'] = 0.01
                param_set['time_length'] = 100000
                param_set['grad_norm_clip'] = 10
                param_set['before_learn'] = 50
                param_set['batch_size'] = 16
                param_set['target_update_interval'] = 400

                # # # iql set
                # param_set['algorithm'] = 'iql_CT'
                # path = '../model/' + map_name + '_iql_CT_3/'

                # COMA set
                param_set['algorithm'] = 'COMA'
                path = '../model/' + map_name + '_COMA_3/'

                param_set['map_name'] = map_name
                param_set['difficulty'] = difficulty
                param_set['path'] = path

                param_set['load_model'] = True
                param_set['test'] = True

                # self.algorithm = MARL()
                # self.algorithmThread = threading.Thread(
                #     target=self.algorithm.algorithm(param_set),
                #     name='StarCraft2Thread')
            """
            # self.algorithm = AlgorithmAgent()
            # self.algorithm.start()

            self.algorithm = MasterAgent()
            self.algorithm.start()

        if globalInformation.get_value('pattern') == strings.HUMAN_VS_MACHINE:
            playWithHuman()
        elif globalInformation.get_value('pattern') == strings.MACHINE_VS_MACHINE:
            playWithMachine()

        # Signal.get_signal().emit_signal_none()

    # pause simulation
    def pauseEvent(self):
        message = 'pause the simulation'
        self.log.info(message)
        Signal.get_signal().emit_signal_str(message)
        if OperationalPlanning.stop:
            return
        if OperationalPlanning.start_or_pause:
            self.qtime.stop()
            OperationalPlanning.start_or_pause = False
        else:
            self.qtime.start(1000)
            OperationalPlanning.start_or_pause = True

    # stop simulation
    def stopEvent(self):
        message = 'stop the simulation'
        self.log.info(message)
        Signal.get_signal().emit_signal_str(message)
        self.qtime.stop()
        OperationalPlanning.start_or_pause = False
        OperationalPlanning.stop = True
        globalInformation.set_value(strings.IS_STOP, True)

    # a description of current map
    def mapEvent(self):
        message = 'open the map description'
        self.log.info(message)
        Signal.get_signal().emit_signal_str(message)
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
        Signal.get_signal().emit_signal_str(message)
        self.window = FramelessWindow('switch policy')
        self.dialog = QDialog()
        # tab item name
        list_str = [
            strings.ALGORITHM_COMA,
            strings.ALGORITHM_COMMNET_COMA,
            strings.ALGORITHM_QMIX,
            strings.ALGORITHM_QTRAN_ALT,
            strings.ALGORITHM_QTRAN_BASE,
            strings.ALGORITHM_VDN
        ]
        # item content
        list_item = [
            strings.CLASS_ALGORITHM_COMA,
            strings.CLASS_ALGORITHM_COMMNET_COMA,
            strings.CLASS_ALGORITHM_QMIX,
            strings.CLASS_ALGORITHM_QTRAN_ALT,
            strings.CLASS_ALGORITHM_QTRAN_BASE,
            strings.CLASS_ALGORITHM_VDN
        ]
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
