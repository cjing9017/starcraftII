"""signal class
@author cj9017
@date 2019/07/05
"""

from PyQt5.QtCore import QObject, pyqtSignal


class Signal(QObject):

    instance = None
    signal = pyqtSignal(str)

    @classmethod
    def get_signal(cls):
        if cls.instance:
            return cls.instance
        else:
            obj = cls()
            cls.instance = obj
            return cls.instance

    def emit_signal(self, message):
        self.signal.emit(message)
