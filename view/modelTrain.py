"""modelTrain
@author: cjing9017
@date: 2019/05/13
"""

from PyQt5.QtWidgets import QWidget, QDialog
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QFrame
from PyQt5.QtWidgets import QPushButton, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDesktopWidget
from PyQt5.Qt import QFont

from resource import globalInformation
from util.getQssFile import GetQssFile
from popupWindow.modelTrainDescriptionDialog import ModelTrainDescriptionDialog


class ModelTrain(QWidget):

    def __init__(self):
        super(ModelTrain, self).__init__()
        self.setObjectName('ModelTrain')
        self.setStyleSheet(GetQssFile.readQss('../resource/qss/modelTrain.qss'))

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

        # model tarin
        self.modelTrain = QPushButton()
        self.modelTrain.setObjectName('modelTrain')
        self.modelTrainLabel = QLabel('model train')
        self.modelTrainLabel.setFont(font)
        self.modelTrain_layout = QVBoxLayout()
        self.modelTrain_layout.addWidget(self.modelTrain, alignment=Qt.AlignCenter)
        self.modelTrain_layout.addWidget(self.modelTrainLabel, alignment=Qt.AlignCenter)
        self.main_layout.addLayout(self.modelTrain_layout)

        # a description dialog
        self.dialog = None

        # add stretch
        self.main_layout.addStretch(1)

        # initialization
        self.initUI()

    def initUI(self):
        self.modelTrain.clicked.connect(self.buttonEvent)

    def buttonEvent(self):
        sender = self.sender()
        if sender == self.modelTrain:
            self.modelTrainEvent()

    def modelTrainEvent(self):
        print('clicked model train in model train')
        self.dialog = QDialog()
        description = "a description of model train"
        model = ModelTrainDescriptionDialog(description)
        model.setupUi(self.dialog)
        self.dialog.setModal(True)
        self.dialog.show()
