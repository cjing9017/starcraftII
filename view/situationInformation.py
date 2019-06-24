"""situationInformation
@author: cjing9017
@date: 2019/05/13
"""

from PyQt5.QtWidgets import QWidget, QDialog
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QFrame
from PyQt5.QtWidgets import QLabel, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDesktopWidget
from PyQt5.Qt import QFont

from resource import globalInformation
from util.getQssFile import GetQssFile
from popupWindow.situationDescriptionDialog import SituationDescriptionDialog


class SituationInformation(QWidget):

    def __init__(self):
        super(SituationInformation, self).__init__()
        self.setObjectName('SituationInformation')
        self.setStyleSheet(GetQssFile.readQss('../resource/qss/situationInformation.qss'))

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

        # consumption action
        self.consumption = QPushButton()
        self.consumption.setObjectName('consumption')
        self.consumptionLabel = QLabel('consumption')
        self.consumptionLabel.setFont(font)
        self.consumption_layout = QVBoxLayout()
        self.consumption_layout.addWidget(self.consumption, alignment=Qt.AlignCenter)
        self.consumption_layout.addWidget(self.consumptionLabel, alignment=Qt.AlignCenter)
        self.main_layout.addLayout(self.consumption_layout)

        # resource action
        self.resource = QPushButton()
        self.resource.setObjectName('resource')
        self.resourceLabel = QLabel('resource')
        self.resourceLabel.setFont(font)
        self.resource_layout = QVBoxLayout()
        self.resource_layout.addWidget(self.resource, alignment=Qt.AlignCenter)
        self.resource_layout.addWidget(self.resourceLabel, alignment=Qt.AlignCenter)
        self.main_layout.addLayout(self.resource_layout)

        # score action
        self.score = QPushButton()
        self.score.setObjectName('score')
        self.scoreLabel = QLabel('score')
        self.scoreLabel.setFont(font)
        self.score_layout = QVBoxLayout()
        self.score_layout.addWidget(self.score, alignment=Qt.AlignCenter)
        self.score_layout.addWidget(self.scoreLabel, alignment=Qt.AlignCenter)
        self.main_layout.addLayout(self.score_layout)

        # output action
        self.output = QPushButton()
        self.output.setObjectName('output')
        self.outputLabel = QLabel('output')
        self.outputLabel.setFont(font)
        self.output_layout = QVBoxLayout()
        self.output_layout.addWidget(self.output, alignment=Qt.AlignCenter)
        self.output_layout.addWidget(self.outputLabel, alignment=Qt.AlignCenter)
        self.main_layout.addLayout(self.output_layout)

        # a description dialog
        self.dialog = None

        # add stretch
        self.main_layout.addStretch(1)

        # initialization
        self.initUI()

    def initUI(self):
        self.consumption.clicked.connect(self.buttonEvent)
        self.score.clicked.connect(self.buttonEvent)
        self.resource.clicked.connect(self.buttonEvent)
        self.output.clicked.connect(self.buttonEvent)

    def buttonEvent(self):
        sender = self.sender()
        if sender == self.consumption:
            self.consumptionEvent()
        elif sender == self.score:
            self.scoreEvent()
        elif sender == self.resource:
            self.resourceEvent()
        elif sender == self.output:
            self.outputEvent()

    def consumptionEvent(self):
        print('clicked consumption in situation infromation')
        self.dialog = QDialog()
        description = "a description of consumption"
        situation = SituationDescriptionDialog(description)
        situation.setupUi(self.dialog)
        self.dialog.setModal(True)
        self.dialog.show()

    def scoreEvent(self):
        print('clicked score in situation information')
        self.dialog = QDialog()
        description = "a description of score"
        situation = SituationDescriptionDialog(description)
        situation.setupUi(self.dialog)
        self.dialog.setModal(True)
        self.dialog.show()

    def resourceEvent(self):
        print('clicked resource in situation information')
        self.dialog = QDialog()
        description = "a description of resource"
        situation = SituationDescriptionDialog(description)
        situation.setupUi(self.dialog)
        self.dialog.setModal(True)
        self.dialog.show()

    def outputEvent(self):
        print('clicked output in situation information')
        self.dialog = QDialog()
        description = "a description of output"
        situation = SituationDescriptionDialog(description)
        situation.setupUi(self.dialog)
        self.dialog.setModal(True)
        self.dialog.show()
