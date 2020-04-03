"""algorithm3
@author: cjing9017
@date: 2019/05/22
"""

from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtWidgets import QHBoxLayout, QFrame, QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDesktopWidget

from util.getQssFile import GetQssFile


class Vdn(QWidget):

    def __init__(self):
        super(Vdn, self).__init__()
        self.setObjectName('Vdn')
        self.setStyleSheet(GetQssFile.readQss('../resource/qss/tabItem.qss'))

        # set widget of layout
        self.frame = QFrame(self)
        self.frame.setGeometry(QDesktopWidget().screenGeometry())
        self.main_layout = QHBoxLayout(self)
        self.setLayout(self.main_layout)

        self.label = QLabel('vdn description')
        self.main_layout.addWidget(self.label, alignment=Qt.AlignCenter)
