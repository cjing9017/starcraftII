"""Custom label class
@author: cjing9017
@date: 2019/05/13
"""
import time
from PyQt5.Qt import QPixmap
from PyQt5.QtWidgets import QSplashScreen


class SplashScreen(QSplashScreen):
    def __init__(self):
        super(SplashScreen, self).__init__(QPixmap("../resource/drawable/logo.jpg"))

    def effect(self):
        self.setWindowOpacity(0)
        t = 0
        while t <= 50:
            new_opacity = self.windowOpacity() + 0.02
            if new_opacity > 1:
                break

            self.setWindowOpacity(new_opacity)
            self.show()
            t -= 1
            time.sleep(0.04)
        time.sleep(1)
        t = 0
        while t <= 50:
            new_opacity = self.windowOpacity() - 0.02
            if new_opacity < 0:
                break
            self.setWindowOpacity(new_opacity)
            t += 1
            time.sleep(0.04)