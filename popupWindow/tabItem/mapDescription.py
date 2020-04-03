"""map description base class
@author: cjing9017
@date: 2019/09/03
"""

from PyQt5.QtWidgets import QWidget, QTextEdit
from PyQt5.QtWidgets import QFrame, QVBoxLayout, QScrollArea
from PyQt5.QtCore import Qt, QTextStream, QFile
from PyQt5.QtWidgets import QDesktopWidget

from util.getQssFile import GetQssFile
from resource import globalInformation


class MapDescription(QWidget):

    def __init__(self, path):
        super(MapDescription, self).__init__()
        self.setObjectName('MapDescription')
        self.setStyleSheet(GetQssFile.readQss('../resource/qss/tabItem.qss'))

        # set widget of layout
        self.frame = QFrame(self)
        self.frame.setGeometry(QDesktopWidget().screenGeometry())
        self.main_layout = QVBoxLayout(self)

        self.text_edit = QTextEdit()
        self.insert_html(path)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(self.text_edit)
        self.scroll_area.setAutoFillBackground(True)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.main_layout.addWidget(self.scroll_area)
        self.setLayout(self.main_layout)

    def insert_html(self, path):
        # f = QFile("./../resource/html/collectMineralsAndGas.html")
        f = QFile(globalInformation.map_name_to_html(path))
        f.open(QFile.ReadOnly | QFile.Text)
        istream = QTextStream(f)
        self.text_edit.setHtml(istream.readAll())
        f.close()
