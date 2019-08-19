"""visualization of fight
@author: cjing9017
@date: 2019/05/13
"""

from PyQt5.QtWidgets import QWidget, QTextEdit, QSizePolicy
from PyQt5.QtWidgets import QLabel, QDesktopWidget, QHBoxLayout
from PyQt5.QtWidgets import QFrame, QPlainTextEdit
from PyQt5.QtGui import QPixmap, QTextDocument
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtWidgets import QApplication

from util.getQssFile import GetQssFile
import win32gui

from util.signal import Signal
import time


class FightView(QWidget):

    # define a signal
    signal = Signal.get_signal().signal

    def __init__(self):
        """

        :rtype:
        """
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
        self.information = QPlainTextEdit(self)
        self.information.setObjectName('information')
        self.information.setPlaceholderText('the output of simulation')
        self.information.setReadOnly(True)
        self.information.setMaximumBlockCount(1000)
        self.information.setLineWrapMode(QPlainTextEdit.WidgetWidth)
        self.information.setFrameShape(QFrame.Panel)
        self.information.setFrameShadow(QFrame.Sunken)
        self.information.setLineWidth(3)
        self.information.setMinimumSize(300, 700)
        self.information.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.information.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.main_layout.addWidget(self.information)

        # set the stretch of two widget
        # self.main_layout.addWidget(self.scroll_area)
        self.main_layout.setStretchFactor(self.view, 3)
        self.main_layout.setStretchFactor(self.information, 1)

        self.setLayout(self.main_layout)

        # initialization
        self.initUI()

    def initUI(self):
        self.signal.connect(self.updateTextMessage)

    def checkWindow(self):
        rect = win32gui.GetWindowRect(self.hwnd)
        self.move(rect[2], rect[1])

    @pyqtSlot(str)
    def updateTextMessage(self, message):
        self.information.appendPlainText('{}: {}'.format(
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), message))
        QApplication.processEvents()
        # time.sleep(1)
