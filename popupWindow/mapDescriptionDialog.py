"""a description of current map
@author: cjing9017
@date: 2019/05/25
"""

from PyQt5 import QtCore
from PyQt5.QtWidgets import QVBoxLayout, QFrame
from PyQt5.QtWidgets import QLabel, QWidget, QSizePolicy
from PyQt5.QtCore import Qt
from PyQt5.Qt import QIcon
from resource import strings
from util.getQssFile import GetQssFile

from resource import globalInformation
from popupWindow.tabItem.mapDescription import MapDescription


class MapDescriptionDialog(QWidget):
    def __init__(self):
        super(MapDescriptionDialog, self).__init__()
        self.main_layout = None
        self.mapLabel = None

    def setupUi(self, Dialog):
        Dialog.setObjectName("MapDescriptionDialog")
        Dialog.resize(700, 600)
        Dialog.setStyleSheet(GetQssFile.readQss('../resource/qss/mapDescriptionDialog.qss'))

        frame = QFrame(Dialog)
        frame.setGeometry(Dialog.geometry())

        main_layout = QVBoxLayout(Dialog, spacing=0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        map_widget = self.getMap()
        main_layout.addWidget(map_widget)
        main_layout.setStretchFactor(map_widget, 1)

        MapDescriptionDialog.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    @staticmethod
    def retranslateUi(Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", strings.OPERATIONAL_PLANNING_TITLE))

    def getMap(self):
        widget = MapDescription(strings.MAP_MOVE_TO_BEACON)
        map_type = globalInformation.get_value(strings.TYPE_MAP)
        if map_type is not None:
            widget = MapDescription(map_type)
        return widget
