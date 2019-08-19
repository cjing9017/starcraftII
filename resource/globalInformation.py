"""store global information
@author: cjing9017
@date: 2019/05/13
"""

from resource import strings
import logging


def init():
    global global_dict
    global_dict = {}
    initArgument()
    log = logging.getLogger('StarCraftII')


def initArgument():
    set_value('current_map_name', strings.DEFAULT_MAP_SMAC)
    set_value('current_algorithm', strings.DEFAULT_ALGORITHM)


def set_value(key, value):
    global_dict[key] = value


def get_value(key, defValue=None):
    try:
        return global_dict[key]
    except KeyError:
        return defValue
