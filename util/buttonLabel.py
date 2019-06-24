"""Custom label class
@author: cjing9017
@date: 2019/05/13
"""


from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QLabel


try:
    _encoding = QApplication.UnicodeUTF8

    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig)


class ButtonLabel(QLabel):
    def __init__(self, parent=None):
        super(ButtonLabel, self).__init__(parent)

    def mousePressEvent(self, e):
        print("you clicked the label")

    def mouseReleaseEvent(self, QMouseEvent):
        print("you have release the mouse")
