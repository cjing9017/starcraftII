"""return the qss file
@author: cjing9017
@date: 2019/05/13
"""


class GetQssFile:

    def __init__(self):
        pass

    @staticmethod
    def readQss(style):
        with open(style, 'r') as f:
            return f.read()
