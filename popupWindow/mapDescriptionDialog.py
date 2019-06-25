"""a description of current map
@author: cjing9017
@date: 2019/05/25
"""

from PyQt5 import QtCore
from PyQt5.QtWidgets import QVBoxLayout, QFrame
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt

from resource import strings
from util.getQssFile import GetQssFile


class MapDescriptionDialog(object):
    def __init__(self):
        super(MapDescriptionDialog, self).__init__()
        self.main_layout = None
        self.mapLabel = None

    def setupUi(self, Dialog):
        Dialog.setObjectName("MapDescriptionDialog")
        Dialog.resize(700, 500)
        Dialog.setStyleSheet(GetQssFile.readQss('../resource/qss/mapDescriptionDialog.qss'))

        self.frame = QFrame(Dialog)
        self.frame.setGeometry(Dialog.geometry())

        self.main_layout = QVBoxLayout(Dialog)
        self.mapLabel = QLabel("a description of current map")
        self.main_layout.addWidget(self.mapLabel, alignment=Qt.AlignCenter)

        MapDescriptionDialog.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    @staticmethod
    def retranslateUi(Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", strings.OPERATIONAL_PLANNING_TITLE))