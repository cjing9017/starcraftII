"""a description of model Train
@author: cjing9017
@date: 2019/05/25
"""

from PyQt5 import QtCore
from PyQt5.QtWidgets import QVBoxLayout, QFrame
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt

from util.getQssFile import GetQssFile


class ModelTrainDescriptionDialog(object):
    def __init__(self, description):
        super(ModelTrainDescriptionDialog, self).__init__()
        self.main_layout = None
        self.mapLabel = None
        self.description = description

    def setupUi(self, Dialog):
        Dialog.setObjectName("ModelTrainDescriptionDialog")
        Dialog.resize(700, 500)
        Dialog.setStyleSheet(GetQssFile.readQss('../resource/qss/modelTrainDescriptionDialog.qss'))

        self.frame = QFrame(Dialog)
        self.frame.setGeometry(Dialog.geometry())

        self.main_layout = QVBoxLayout(Dialog)
        self.mapLabel = QLabel(self.description)
        self.main_layout.addWidget(self.mapLabel, alignment=Qt.AlignCenter)

        ModelTrainDescriptionDialog.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    @staticmethod
    def retranslateUi(Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Model Train"))