"""scroll widget
@author: cjing9017
@date: 2019/07/04
"""

from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtWidgets import QHBoxLayout, QFrame, QVBoxLayout, QScrollArea
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDesktopWidget, QGridLayout

from util.getQssFile import GetQssFile


class ScrollWidget(QWidget):

    def __int__(self, **kwargs):
        super(ScrollWidget, self).__init__()
        self.setObjectName('ScrollWidget')

        self.description = kwargs['description']
        self.initial_state = kwargs['initial_state']
        self.rewards = kwargs['rewards']
        self.end_condition = kwargs['end_condition']
        self.time_limit = kwargs['time_limit']
        self.additional_notes = kwargs['additional_notes']

        self.main_layout = QGridLayout()
        self.setLayout(self.main_layout)

        self.initUi(self.calculate_row(), 1)

    def initUi(self, rows, cols):
        pass

    def calculate_row(self):
        count = 0

        count += len(self.description)
        count += len(self.initial_state)
        count += len(self.rewards)
        count += len(self.end_condition)
        count += len(self.time_limit)
        count += len(self.additional_notes)

        return count

