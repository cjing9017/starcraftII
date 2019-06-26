"""replay
@author: cjing9017
@date: 2019/05/13
"""

from PyQt5 import QtCore
from PyQt5.QtWidgets import QVBoxLayout, QFrame

from resource import strings

from popupWindow.videoBox import VideoBox
from util.getQssFile import GetQssFile


class ViewDialog(object):
    def __init__(self):
        super(ViewDialog, self).__init__()
        self.main_layout = None
        self.box = None
        # use to create a listWidget

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(700, 500)
        Dialog.setStyleSheet(GetQssFile.readQss('../resource/qss/viewDialog.qss'))

        self.frame = QFrame(Dialog)
        self.frame.setGeometry(Dialog.geometry())

        self.main_layout = QVBoxLayout(Dialog)
        self.box = VideoBox('../resource/videos/testvideo.mp4')
        self.main_layout.addWidget(self.box)

        ViewDialog.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    @staticmethod
    def retranslateUi(Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", strings.REPLAY_TITLE))
