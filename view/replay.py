"""replay
@author: cjing9017
@date: 2019/05/13
"""

from PyQt5.QtWidgets import QWidget, QDockWidget, QDialog
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QFrame
from PyQt5.QtWidgets import QPushButton, QLabel
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QDesktopWidget
from PyQt5.Qt import QFont, QIcon

from resource import globalInformation
from util.getQssFile import GetQssFile
from popupWindow.viewDialog import ViewDialog

from barWindow.frameLessWindow import FramelessWindow


class Replay(QWidget):

    def __init__(self):
        super(Replay, self).__init__()
        self.setObjectName('Replay')
        self.setStyleSheet(GetQssFile.readQss('../resource/qss/replay.qss'))

        # font
        font = QFont()
        font.setWeight(50)
        font.setPixelSize(15)

        # dockView for replay
        self.replayView = None

        # set widget of layout
        self.frame = QFrame(self)
        self.frame.setGeometry(QDesktopWidget().screenGeometry())
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setSpacing(20)
        self.setLayout(self.main_layout)

        # replay action
        self.replay = QPushButton()
        self.replay.setObjectName('replay')
        self.replayLabel = QLabel('replay')
        self.replayLabel.setFont(font)
        self.replay_layout = QVBoxLayout()
        self.replay_layout.addWidget(self.replay, alignment=Qt.AlignCenter)
        self.replay_layout.addWidget(self.replayLabel, alignment=Qt.AlignCenter)
        self.main_layout.addLayout(self.replay_layout)

        # add stretch
        self.main_layout.addStretch(1)

        # initialization
        self.initUI()

    def initUI(self):
        self.replay.clicked.connect(self.buttonEvent)

    def buttonEvent(self):
        sender = self.sender()
        if sender == self.replay:
            self.replayEvent()

    def replayEvent(self):
        print('clicked replay in replay')
        self.window = FramelessWindow('replay')
        self.replayView = QDialog()
        listDialog = ViewDialog()
        listDialog.setupUi(self.replayView)
        self.window.setWidget(self.replayView)
        self.initFrameLessWindow(QSize(700, 600), 'Replay', QIcon('../resource/drawable/logo.png'))
        self.window.show()
        # self.replayView.setModal(True)
        # self.replayView.show()

    def initFrameLessWindow(self, size, title, icon):
        self.window.resize(size)
        self.window.setWindowTitle(title)
        self.window.setWindowIcon(icon)
