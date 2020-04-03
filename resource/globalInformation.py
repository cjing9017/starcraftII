"""store global information
@author: cjing9017
@date: 2019/05/13
"""

from resource import strings
import logging
import json


def init():
    global global_dict
    global map_to_html
    global_dict = {}
    map_to_html = {}
    initArgument()
    log = logging.getLogger('StarCraftII')


def initArgument():
    set_value('current_map_name', strings.DEFAULT_MAP_SMAC)
    set_value('current_algorithm', strings.DEFAULT_ALGORITHM)
    set_value(strings.IS_STOP, True)

    # define map name to map class
    set_value(strings.MAP_MOVE_TO_BEACON, strings.CLASS_MAP_MOVE_TO_BEACON)
    set_value(strings.MAP_COLLECT_MINERAL_SHARDS, strings.CLASS_MAP_COLLECT_MINERAL_SHARDS)
    set_value(strings.MAP_FIND_AND_DEFEAT_ZERGLINGS, strings.CLASS_MAP_FIND_AND_DEFEAT_ZERGLINGS)
    set_value(strings.MAP_DEFEAT_ROACHES, strings.CLASS_MAP_DEFEAT_ROACHES)
    set_value(strings.MAP_DEFEAT_ZERGLINGS_AND_BANELINGS, strings.CLASS_MAP_DEFEAT_ZERGLINGS_AND_BANELINGS)
    set_value(strings.MAP_COLLECT_MINERALS_AND_GAS, strings.CLASS_MAP_COLLECT_MINERALS_AND_GAS)
    set_value(strings.MAP_BUILD_MARINES, strings.CLASS_MAP_BUILD_MARINES)

    init_map_html()

    init_alg_map()


def init_alg_map():
    with open("../resource/algorithm_map.json", "r") as f:
        json_str = json.load(f)
        alg_map_dict = json.loads(json_str)
        set_value(strings.ALGORITHM_MAP, alg_map_dict)


def init_map_html():
    map_to_html[strings.MAP_MOVE_TO_BEACON] = './../resource/html/moveToBeacon.html'
    map_to_html[strings.MAP_COLLECT_MINERAL_SHARDS] = './../resource/html/collectMineralShards.html'
    map_to_html[strings.MAP_FIND_AND_DEFEAT_ZERGLINGS] = './../resource/html/findAndDefeatZerglings.html'
    map_to_html[strings.MAP_DEFEAT_ROACHES] = './../resource/html/defeatRoaches.html'
    map_to_html[strings.MAP_DEFEAT_ZERGLINGS_AND_BANELINGS] = './../resource/html/defeatZerglingsAndBanelings.html'
    map_to_html[strings.MAP_COLLECT_MINERALS_AND_GAS] = './../resource/html/collectMineralsAndGas.html'
    map_to_html[strings.MAP_BUILD_MARINES] = './../resource/html/buildMarines.html'

    map_to_html[strings.MAP_2C_VS_64ZG] = './../resource/html/2c_vs_64zg.html'
    map_to_html[strings.MAP_2M_VS_1Z] = './../resource/html/2m_vs_1z.html'
    map_to_html[strings.MAP_2S3Z] = './../resource/html/2s3z.html'
    map_to_html[strings.MAP_2S_VS_1SC] = './../resource/html/2s_vs_1sc.html'
    map_to_html[strings.MAP_3M] = './../resource/html/3m.html'
    map_to_html[strings.MAP_3S5Z] = './../resource/html/3s5z.html'
    map_to_html[strings.MAP_3S5Z_VS_3S6Z] = './../resource/html/3s5z_vs_3s6z.html'
    map_to_html[strings.MAP_3S_VS_3Z] = './../resource/html/3s_vs_3z.html'
    map_to_html[strings.MAP_3S_VS_4Z] = './../resource/html/3s_vs_4z.html'
    map_to_html[strings.MAP_3S_VS_5Z] = './../resource/html/3s_vs_5z.html'
    map_to_html[strings.MAP_5M_VS_6M] = './../resource/html/5m_vs_6m.html'
    map_to_html[strings.MAP_6H_VS_8Z] = './../resource/html/6h_vs_8z.html'
    map_to_html[strings.MAP_8M] = './../resource/html/8m.html'
    map_to_html[strings.MAP_8M_VS_9M] = './../resource/html/8m_vs_9m.html'
    map_to_html[strings.MAP_10M_VS_11M] = './../resource/html/10m_vs_11m.html'
    map_to_html[strings.MAP_25M] = './../resource/html/25m.html'
    map_to_html[strings.MAP_27M_VS_30M] = './../resource/html/27m_vs_30m.html'
    map_to_html[strings.MAP_BANE_VS_BANE] = './../resource/html/bane_vs_bane.html'
    map_to_html[strings.MAP_CORRIDOR] = './../resource/html/corridor.html'
    map_to_html[strings.MAP_MMM] = './../resource/html/MMM.html'
    map_to_html[strings.MAP_MMM2] = './../resource/html/MMM2.html'
    map_to_html[strings.MAP_SO_MANY_BANELINGS] = './../resource/html/so_many_banelings.html'
    map_to_html[strings.CONFIGURATION_INFORMATION] = './../resource/html/configurationInformation.html'


def set_value(key, value):
    global_dict[key] = value


def get_value(key, defValue=None):
    try:
        return global_dict[key]
    except KeyError:
        return defValue


def map_name_to_html(map_name):
    return map_to_html[map_name]
