"""maps
@author: cjing9017
@date: 2019/05/13
"""

from PyQt5.QtWidgets import QWidget, QDialog
from PyQt5.QtWidgets import QPushButton, QLabel
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QFrame
from PyQt5.QtWidgets import QDesktopWidget
from PyQt5.QtCore import Qt
from PyQt5.Qt import QFont

import os

from resource import globalInformation
from util.getQssFile import GetQssFile
from resource import strings
from popupWindow.listDialog import ListDialog


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
        print('clicked choose map in maps')
        self.dialog = QDialog()
        # tab item name
        list_str = [strings.MAP1, strings.MAP2, strings.MAP3]
        # item content
        list_item = [strings.CLASS_MAP1, strings.CLASS_MAP2, strings.CLASS_MAP3]
        # title name
        title = strings.MAPS_TITLE
        listDialog = ListDialog(list_str, list_item, title)
        listDialog.setupUi(self.dialog)
        self.dialog.setModal(True)
        self.dialog.show()

    @staticmethod
    def mapDesignEvent():
        print('clicked map design in maps')
        os.system(strings.SCMDRAFT)
