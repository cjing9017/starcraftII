"""signal class
@author cj9017
@date 2019/07/05
"""

from PyQt5.QtCore import QObject, pyqtSignal


class Signal(QObject):

    instance = None
    signal_str = pyqtSignal(str)
    signal_none = pyqtSignal()
    signal_gameover = pyqtSignal()
    signal_game_pause = pyqtSignal(int)

    @classmethod
    def get_signal(cls):
        if cls.instance:
            return cls.instance
        else:
            obj = cls()
            cls.instance = obj
            return cls.instance

    def emit_signal_str(self, message):
        self.signal_str.emit(message)

    def emit_signal_none(self):
        self.signal_none.emit()

    def emit_signal_gameover(self):
        self.signal_gameover.emit()

    def emit_signal_game_pause(self, pause):
        self.signal_game_pause.emit(pause)
