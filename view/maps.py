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
        font = QFont("Roman times",36,QFont.Bold)
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
        Signal.get_signal().emit_signal(message)
        self.window = FramelessWindow('choose map')
        self.dialog = QDialog()
        # tab item name
        list_str = [
            strings.MAP_MOVE_TO_BEACON,
            strings.MAP_COLLECT_MINERAL_SHARDS,
            strings.MAP_FIND_AND_DEFEAT_ZERGLINGS,
            strings.MAP_DEFEAT_ROACHES,
            strings.MAP_DEFEAT_ZERGLINGS_AND_BANELINGS,
            strings.MAP_COLLECT_MINERALS_AND_GAS,
            strings.MAP_BUILD_MARINES
        ]
        # item content
        list_item = [
            strings.CLASS_MAP_MOVE_TO_BEACON,
            strings.CLASS_MAP_COLLECT_MINERAL_SHARDS,
            strings.CLASS_MAP_FIND_AND_DEFEAT_ZERGLINGS,
            strings.CLASS_MAP_DEFEAT_ROACHES,
            strings.CLASS_MAP_DEFEAT_ZERGLINGS_AND_BANELINGS,
            strings.CLASS_MAP_COLLECT_MINERALS_AND_GAS,
            strings.CLASS_MAP_BUILD_MARINES
        ]
        # title name
        self.listDialog = ListDialog(list_str, list_item, strings.MAPS_TITLE, strings.TYPE_MAP)
        self.listDialog.setupUi(self.dialog, self.window)
        self.window.setWidget(self.dialog)
        self.initFrameLessWindow(
            QSize(700, 600),
            'Maps',
            QIcon('../resource/drawable/logo.png')
        )
        self.window.show()
        # self.dialog.setModal(True)
        # self.dialog.show()

    @staticmethod
    def mapDesignEvent():
        message = 'open the map designer to customize the map'
        log = logging.getLogger('StarCraftII')
        log.info(message)
        Signal.get_signal().emit_signal(message)
        # os.system(strings.SCMDRAFT)
        subprocess.Popen(strings.SCMDRAFT)

    def initFrameLessWindow(self, size, title, icon):
        self.window.resize(size)
        self.window.setWindowTitle(title)
        self.window.setWindowIcon(icon)
