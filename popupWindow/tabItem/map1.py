"""map1
@author: cjing9017
@date: 2019/05/25
"""

from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtWidgets import QHBoxLayout, QFrame, QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDesktopWidget

from util.getQssFile import GetQssFile


class Map1(QWidget):

    def __init__(self):
        super(Map1, self).__init__()
        self.setObjectName('Map1')
        self.setStyleSheet(GetQssFile.readQss('../resource/qss/tabItem.qss'))

        # set widget of layout
        self.frame = QFrame(self)
        self.frame.setGeometry(QDesktopWidget().screenGeometry())
        self.main_layout = QVBoxLayout(self)
        self.setLayout(self.main_layout)

        self.label = QLabel('map1 description')
        self.main_layout.addWidget(self.label, alignment=Qt.AlignCenter)