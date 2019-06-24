"""store global information
@author: cjing9017
@date: 2019/05/13
"""


def init():
    global global_dict
    global_dict = {}
    initArgument()


def initArgument():
    pass


def set_value(key, value):
    global_dict[key] = value


def get_value(key, defValue=None):
    try:
        return global_dict[key]
    except KeyError:
        return defValue
