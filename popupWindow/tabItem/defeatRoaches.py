"""map: defeat roaches
@author: cjing9017
@date: 2019/05/25
"""

from PyQt5.QtWidgets import QWidget, QLabel, QTextEdit, QTextBrowser
from PyQt5.QtWidgets import QHBoxLayout, QFrame, QVBoxLayout, QScrollArea
from PyQt5.QtCore import Qt, QTextStream, QFile
from PyQt5.QtWidgets import QDesktopWidget

from util.getQssFile import GetQssFile


class DefeatRoaches(QWidget):

    def __init__(self):
        super(DefeatRoaches, self).__init__()
        self.setObjectName('DefeatRoaches')
        self.setStyleSheet(GetQssFile.readQss('../resource/qss/tabItem.qss'))

        # set widget of layout
        self.frame = QFrame(self)
        self.frame.setGeometry(QDesktopWidget().screenGeometry())
        self.main_layout = QVBoxLayout(self)

        self.text_edit = QTextEdit()
        self.insert_html()

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(self.text_edit)
        self.scroll_area.setAutoFillBackground(True)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.main_layout.addWidget(self.scroll_area)
        self.setLayout(self.main_layout)
        # self.main_layout.addWidget(self.label, alignment=Qt.AlignCenter)

    def insert_html(self):
        f = QFile("./../resource/html/defeatRoaches.html")
        f.open(QFile.ReadOnly | QFile.Text)
        istream = QTextStream(f)
        self.text_edit.setHtml(istream.readAll())
        f.close()