"""maps
@author: cjing9017
@date: 2019/05/13
"""

from PyQt5.QtWidgets import QWidget, QDialog
from PyQt5.QtWidgets import QPushButton, QLabel
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QFrame
from PyQt5.QtWidgets import QDesktopWidget
from PyQt5.QtCore import Qt, QSize
from PyQt5.Qt import QFont, QIcon

import os

from resource import globalInformation
from util.getQssFile import GetQssFile
from resource import strings
from popupWindow.listDialog import ListDialog

from barWindow.frameLessWindow import FramelessWindow
from util.signal import Signal
import subprocess

from util.logs import Log
import logging


class Maps(QWidget):

    def __init__(self):
        super(Maps, self).__init__()
        self.setObjectName('Maps')
        self.setStyleSheet(GetQssFile.readQss('../resource/qss/maps.qss'))

        # font
        font = QFont("Roman times", 36, QFont.Bold)
        # font.setWeight(50)
        # font.setFamily('Helvetica')
        font.setPixelSize(15)

        # set widget of layout
        self.frame = QFrame(self)
        self.frame.setGeometry(QDesktopWidget().screenGeometry())
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setSpacing(20)
        self.setLayout(self.main_layout)

        # choose map
        self.chooseMap = QPushButton()
        self.chooseMap.setObjectName('chooseMap')
        self.chooseMapLabel = QLabel('choose map')
        self.chooseMapLabel.setFont(font)
        self.chooseMap_layout = QVBoxLayout()
        self.chooseMap_layout.addWidget(self.chooseMap, alignment=Qt.AlignCenter)
        self.chooseMap_layout.addWidget(self.chooseMapLabel, alignment=Qt.AlignCenter)
        self.main_layout.addLayout(self.chooseMap_layout)

        # map design
        self.mapDesign = QPushButton()
        self.mapDesign.setObjectName('mapDesign')
        self.mapDesignLabel = QLabel('map design')
        self.mapDesignLabel.setFont(font)
        self.mapDesign_layout = QVBoxLayout()
        self.mapDesign_layout.addWidget(self.mapDesign, alignment=Qt.AlignCenter)
        self.mapDesign_layout.addWidget(self.mapDesignLabel, alignment=Qt.AlignCenter)
        self.main_layout.addLayout(self.mapDesign_layout)

        # dialog
        self.dialog = None

        # add stretch
        self.main_layout.addStretch(1)

        # initialization
        self.initUI()

        self.list_str = [
            strings.MAP_MOVE_TO_BEACON,
            strings.MAP_COLLECT_MINERAL_SHARDS,
            strings.MAP_FIND_AND_DEFEAT_ZERGLINGS,
            strings.MAP_DEFEAT_ROACHES,
            strings.MAP_DEFEAT_ZERGLINGS_AND_BANELINGS,
            strings.MAP_COLLECT_MINERALS_AND_GAS,
            strings.MAP_BUILD_MARINES,
            strings.MAP_2C_VS_64ZG,
            strings.MAP_2M_VS_1Z,
            strings.MAP_2S3Z,
            strings.MAP_2S_VS_1SC,
            strings.MAP_3M,
            strings.MAP_3S5Z,
            strings.MAP_3S5Z_VS_3S6Z,
            strings.MAP_3S_VS_3Z,
            strings.MAP_3S_VS_4Z,
            strings.MAP_3S_VS_5Z,
            strings.MAP_5M_VS_6M,
            strings.MAP_6H_VS_8Z,
            strings.MAP_8M,
            strings.MAP_8M_VS_9M,
            strings.MAP_10M_VS_11M,
            strings.MAP_25M,
            strings.MAP_27M_VS_30M,
            strings.MAP_BANE_VS_BANE,
            strings.MAP_CORRIDOR,
            strings.MAP_MMM,
            strings.MAP_MMM2,
            strings.MAP_SO_MANY_BANELINGS
        ]

    def initUI(self):
        self.chooseMap.clicked.connect(self.buttonEvent)
        self.mapDesign.clicked.connect(self.buttonEvent)

    def buttonEvent(self):
        sender = self.sender()
        if sender == self.chooseMap:
            self.chooseMapEvent()
        elif sender == self.mapDesign:
            Maps.mapDesignEvent()

    def chooseMapEvent(self):
        message = 'choose new map'
        log = logging.getLogger('StarCraftII')
        log.info(message)
        Signal.get_signal().emit_signal_str(message)
        self.window = FramelessWindow('choose map')
        self.dialog = QDialog()
        # tab item name
        list_map = self.list_str if globalInformation.get_value(strings.TYPE_POLICY) is None \
            else globalInformation.get_value(strings.ALGORITHM_MAP)[globalInformation.get_value(strings.TYPE_POLICY)]
        # title name
        self.listDialog = ListDialog(list_map, None, strings.MAPS_TITLE, strings.TYPE_MAP)
        self.listDialog.setupUi(self.dialog, self.window)
        self.window.setWidget(self.dialog)
        self.initFrameLessWindow(
            QSize(700, 600),
            'Maps',
            QIcon('../resource/drawable/logo.png')
        )
        self.dialog.setModal(True)

        self.window.show()
        # self.dialog.setModal(True)
        # self.dialog.show()

    @staticmethod
    def mapDesignEvent():
        message = 'open the map designer to customize the map'
        log = logging.getLogger('StarCraftII')
        log.info(message)
        Signal.get_signal().emit_signal_str(message)
        # os.system(strings.SCMDRAFT)
        subprocess.Popen(strings.SCMDRAFT)

    def initFrameLessWindow(self, size, title, icon):
        self.window.resize(size)
        self.window.setWindowTitle(title)
        self.window.setWindowIcon(icon)
