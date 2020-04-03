from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QApplication


class TimeWorker(QThread):

    def __init__(self, widget, interval):
        super(TimeWorker, self).__init__()
        self.widget = widget
        self.interval = interval

    def run(self):
        if self.interval > 0:
            days = self.interval // (24 * 60 * 60)
            hour = (self.interval - days * 24 * 60 * 60) // (60 * 60)
            min = (self.interval - days * 24 * 60 * 60 - hour * 60 * 60) // 60
            sec = self.interval - days * 24 * 60 * 60 - hour * 60 * 60 - min * 60
            intervals = str(hour) + ':' + str(min) + ':' + str(sec)
            self.widget.display(intervals)
            QApplication.processEvents()
