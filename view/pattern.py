"""item1
@author: cjing9017
@date: 2019/05/13
"""

from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QHBoxLayout, QFrame
from PyQt5.QtWidgets import QRadioButton, QButtonGroup
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDesktopWidget
from PyQt5.Qt import QFont

from resource import strings
from util.getQssFile import GetQssFile
from resource import globalInformation


class Pattern(QWidget):

    def __init__(self):
        super(Pattern, self).__init__()
        self.setObjectName('Pattern')
        self.setStyleSheet(GetQssFile.readQss('../resource/qss/pattern.qss'))

        # set widget of layout
        self.frame = QFrame(self)
        self.frame.setGeometry(QDesktopWidget().screenGeometry())
        self.main_layout = QHBoxLayout(self)
        self.human_machine = QRadioButton(strings.HUMAN_VS_MACHINE, self.frame)
        self.machine_machine = QRadioButton(strings.MACHINE_VS_MACHINE, self.frame)
        self.vs_group = QButtonGroup(self.frame)
        self.main_layout.addWidget(self.human_machine, alignment=Qt.AlignCenter)
        self.main_layout.addWidget(self.machine_machine, alignment=Qt.AlignCenter)
        self.main_layout.addStretch(1)
        self.setLayout(self.main_layout)

        # initialization
        self.initUI()

    def initUI(self):
        font = QFont()
        font.setWeight(50)
        font.setPixelSize(15)
        self.human_machine.setFont(font)
        self.machine_machine.setFont(font)
        self.vs_group.addButton(self.human_machine, 1)
        self.vs_group.addButton(self.machine_machine, 2)
        self.vs_group.buttonClicked.connect(self.radioClicked)

    # the slot function of radio group
    def radioClicked(self):
        sender = self.sender()
        if sender == self.vs_group:
            if self.vs_group.checkedId() == 1:
                print("clicked human vs. machine in pattern")
                globalInformation.set_value('pattern', strings.HUMAN_VS_MACHINE)
            elif self.vs_group.checkedId() == 2:
                print("clicked machine vs. machine in pattern")
                globalInformation.set_value('pattern', strings.MACHINE_VS_MACHINE)
