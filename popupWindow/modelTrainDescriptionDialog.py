"""a description of model Train
@author: cjing9017
@date: 2019/05/25
"""

from PyQt5 import QtCore
from PyQt5.QtWidgets import QVBoxLayout, QFrame
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt

from resource import strings
from resource import globalInformation
from popupWindow.tabItem.mapDescription import MapDescription
from util.writeHtml import WriteHtml
from util.getQssFile import GetQssFile


class ModelTrainDescriptionDialog(object):
    def __init__(self, description):
        super(ModelTrainDescriptionDialog, self).__init__()
        self.main_layout = None
        self.mapLabel = None
        self.description = description

    def setupUi(self, Dialog):
        Dialog.setObjectName("ModelTrainDescriptionDialog")
        Dialog.resize(700, 600)
        Dialog.setStyleSheet(GetQssFile.readQss('../resource/qss/modelTrainDescriptionDialog.qss'))

        frame = QFrame(Dialog)
        frame.setGeometry(Dialog.geometry())

        main_layout = QVBoxLayout(Dialog, spacing=0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        description_widget = self.get_description_widget()
        main_layout.addWidget(description_widget)
        main_layout.setStretchFactor(description_widget, 1)

        ModelTrainDescriptionDialog.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    @staticmethod
    def retranslateUi(Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Model Train"))

    def get_description_widget(self):
        type_pattern = globalInformation.get_value(strings.TYPE_PATTERN)
        type_policy = globalInformation.get_value(strings.TYPE_POLICY)
        type_map = globalInformation.get_value(strings.TYPE_MAP)
        html = WriteHtml(type_pattern, type_policy, type_map)
        html.write_html()

        return MapDescription(strings.CONFIGURATION_INFORMATION)
