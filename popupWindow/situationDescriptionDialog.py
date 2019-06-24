"""a description of  situation
@author: cjing9017
@date: 2019/05/25
"""

from PyQt5 import QtCore
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt


class SituationDescriptionDialog(object):
    def __init__(self, description):
        super(SituationDescriptionDialog, self).__init__()
        self.main_layout = None
        self.mapLabel = None
        self.description = description

    def setupUi(self, Dialog):
        Dialog.setObjectName("SituationDescriptionDialog")
        Dialog.resize(700, 500)
        self.main_layout = QVBoxLayout(Dialog)
        self.mapLabel = QLabel(self.description)
        self.main_layout.addWidget(self.mapLabel, alignment=Qt.AlignCenter)

        SituationDescriptionDialog.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    @staticmethod
    def retranslateUi(Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Situation Information"))