"""algorithm2
@author: cjing9017
@date: 2019/05/22
"""

from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtWidgets import QHBoxLayout, QFrame, QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDesktopWidget

from util.getQssFile import GetQssFile


class Algorithm2(QWidget):

    def __init__(self):
        super(Algorithm2, self).__init__()
        self.setObjectName('Algorithm2')
        self.setStyleSheet(GetQssFile.readQss('../resource/qss/tabItem.qss'))

        # set widget of layout
        self.frame = QFrame(self)
        self.frame.setGeometry(QDesktopWidget().screenGeometry())
        self.main_layout = QHBoxLayout(self)
        self.setLayout(self.main_layout)

        self.label = QLabel('algorithm2 description')
        self.main_layout.addWidget(self.label, alignment=Qt.AlignCenter)
