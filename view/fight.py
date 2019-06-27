"""visualization of fight
@author: cjing9017
@date: 2019/05/13
"""

from PyQt5.QtWidgets import QWidget, QTextEdit, QSizePolicy
from PyQt5.QtWidgets import QLabel, QHBoxLayout, QDesktopWidget
from PyQt5.QtWidgets import QFrame
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QRect
from PyQt5.QtCore import Qt

from util.getQssFile import GetQssFile


class FightView(QWidget):

    def __init__(self):
        super(FightView, self).__init__()
        self.setObjectName('FightView')

        self.setStyleSheet(GetQssFile.readQss('../resource/qss/fight.qss'))

        # set the size attribute
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)

        self.frame = QFrame(self)
        self.frame.setGeometry(QDesktopWidget().screenGeometry())

        # set main layout
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(10, 10, 10, 20)
        self.main_layout.setSpacing(10)
        # set widget of layout
        self.view = QLabel(self)
        self.view.setObjectName('view')
        self.view.setScaledContents(True)
        self.view.setPixmap(QPixmap('../resource/drawable/view.png'))
        self.view.setMinimumSize(600, 700)
        self.main_layout.addWidget(self.view)
        self.information = QTextEdit(self)
        self.information.setObjectName('information')
        self.information.setPlaceholderText('the output of simulation')
        self.information.setEnabled(False)
        self.information.setFrameShape(QFrame.Panel)
        self.information.setFrameShadow(QFrame.Sunken)
        self.information.setLineWidth(3)
        self.information.setMinimumSize(300, 700)

        # set the stretch of two widget
        self.main_layout.addWidget(self.information)
        self.main_layout.setStretchFactor(self.view, 3)
        self.main_layout.setStretchFactor(self.information, 1)

        self.setLayout(self.main_layout)

        # initialization
        self.initUI()

    def initUI(self):
        pass
