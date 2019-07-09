"""log class
@author: cj9017
@date: 2019/07/04
"""

import logging
import logging.handlers
from datetime import datetime


class Log:

    log = logging.getLogger('StarCraftII')
    log.setLevel(logging.DEBUG)

    # define handler for writing log file
    date = datetime.now()
    file_log = logging.handlers.TimedRotatingFileHandler(
        filename='../resource/logs/{}'.format(date.strftime('%Y-%m-%d')),
        when='h',
        interval=1,
        backupCount=10,
    )
    file_log.setLevel(logging.DEBUG)

    # define handler for print log to console
    print_log = logging.StreamHandler()
    print_log.setLevel(logging.DEBUG)

    # print formatter
    formatter = logging.Formatter(
        fmt='%(asctime)s %(name)s %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S %p'
    )

    file_log.setFormatter(formatter)
    print_log.setFormatter(formatter)

    log.addHandler(file_log)
    log.addHandler(print_log)
