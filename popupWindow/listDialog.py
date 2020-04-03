"""custom dialog for list item
@author: cjing9017
@date: 2019/05/22
"""

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QFrame
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QAbstractButton
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QListWidget, QStackedWidget, QListWidgetItem
from PyQt5.Qt import QFont

from util.getQssFile import GetQssFile
import logging
from util.signal import Signal
from resource import strings
from resource import globalInformation
from util.logs import Log

# the description of algorithm
from popupWindow.tabItem.coma import Coma
from popupWindow.tabItem.commnet_coma import CommnetComa
from popupWindow.tabItem.qmix import Qmix
from popupWindow.tabItem.qtran_alt import QtranAlt
from popupWindow.tabItem.qtran_base import QtranBase
from popupWindow.tabItem.vdn import Vdn

from popupWindow.tabItem.mapDescription import MapDescription

# from common.Config import *


class ListDialog(object):
    def __init__(self, list_str, list_item, title, name):
        super(ListDialog, self).__init__()
        self.buttonBox = None
        self.main_layout = None
        self.tab_layout = None
        self.tab_widget = None
        self.item_widget = None

        # use to create a listWidget
        self.list_str = list_str
        self.list_item = list_item
        self.title = title
        self.name = name

        # store old value of map and policy
        self.type_map = globalInformation.get_value(strings.TYPE_MAP)
        self.type_policy = globalInformation.get_value(strings.TYPE_POLICY)

    def setupUi(self, Dialog, window):
        Dialog.setObjectName("Dialog")
        Dialog.resize(700, 600)

        Dialog.setWindowTitle(self.title)
        Dialog.setStyleSheet(GetQssFile.readQss('../resource/qss/listDialog.qss'))
        self.main_layout = QVBoxLayout(Dialog)

        self.frame = QFrame(Dialog)
        self.frame.setGeometry(Dialog.geometry())

        self.tab_layout = QHBoxLayout(spacing=0)
        self.tab_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.addLayout(self.tab_layout)

        # left tab
        self.tab_widget = QListWidget()
        self.tab_widget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.tab_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.tab_widget.setFrameShape(QListWidget.NoFrame)
        self.tab_layout.addWidget(self.tab_widget)
        # tab item
        self.item_widget = QStackedWidget()
        self.tab_layout.addWidget(self.item_widget)
        self.tab_layout.setStretchFactor(self.tab_widget, 1)
        self.tab_layout.setStretchFactor(self.item_widget, 4)
        self.initTab()

        self.buttonBox = QtWidgets.QDialogButtonBox()
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.confirm = self.buttonBox.addButton(QtWidgets.QDialogButtonBox.Ok)
        self.confirm.setText('confirm')
        self.cancel = self.buttonBox.addButton(QtWidgets.QDialogButtonBox.Cancel)
        self.cancel.setText('cancel')
        self.buttonBox.setObjectName("buttonBox")
        self.main_layout.addWidget(self.buttonBox, alignment=Qt.AlignRight)

        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.accepted.connect(window.close)
        self.buttonBox.accepted.connect(self.button_confirm)
        self.buttonBox.rejected.connect(Dialog.reject)
        self.buttonBox.rejected.connect(window.close)
        self.buttonBox.rejected.connect(self.button_cancel)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def button_confirm(self):
        pass

    def button_cancel(self):
        if self.name == strings.TYPE_POLICY:
            globalInformation.set_value(strings.TYPE_POLICY, self.type_policy)
        elif self.name == strings.TYPE_MAP:
            globalInformation.set_value(strings.TYPE_MAP, self.type_map)

    def initTab(self):
        # connect tab and item
        self.tab_widget.currentRowChanged.connect(self.item_widget.setCurrentIndex)
        self.tab_widget.currentRowChanged.connect(self.map_choose)
        for i in range(len(self.list_str)):
            # add item to tab
            font = QFont()
            font.setBold(True)
            font.setWeight(50)
            font.setPixelSize(14)

            item = QListWidgetItem(self.list_str[i], self.tab_widget)
            item.setSizeHint(QSize(30, 50))
            item.setFont(font)
            item.setTextAlignment(Qt.AlignCenter)
            if i == 0:
                item.setSelected(True)
            # add item content
            if self.name == strings.TYPE_POLICY:
                self.item_widget.addWidget(eval(self.list_item[i]))
            elif self.name == strings.TYPE_MAP:
                self.item_widget.addWidget(MapDescription(self.list_str[i]))

    def map_choose(self, row):
        message = 'choose {}: {}'.format(self.name, self.list_str[row])
        log = logging.getLogger('StarCraftII')
        log.info(message)
        Signal.get_signal().emit_signal_str(message)
        if self.name == strings.TYPE_POLICY:
            globalInformation.set_value(strings.TYPE_POLICY, self.list_str[row])
        elif self.name == strings.TYPE_MAP:
            globalInformation.set_value(strings.TYPE_MAP, self.list_str[row])
