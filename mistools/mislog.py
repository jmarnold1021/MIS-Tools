"""
Module for retriving various loggers. Currently there is only one console handelr.
"""

import logging

# create logger
# below has some good guidelines on when to use what levels...
# https://docs.python.org/3/howto/logging.html#logging-levels
def mis_console_logger(name, level):

    '''
    Retrive a new instance of a Console logger

    :param str name: The name of the logger good for differenting between libraries/methods/commands etc

    :param str level: The log level. Choices:['DEBUG','INFO','WARNING','WARN','ERROR','CRITICAL'] default: 'INFO'

    :return: Instance of console logger

    :rtype: Object

    '''

    # create logging comps
    logger = logging.getLogger(name)
    handler = logging.StreamHandler() # log to console
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s') # sort of verbose atm

    # link everything
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    LOG_LEVELS = {

        "CRITICAL" : '50',
        "ERROR"    : '40',
        "WARNING"  : '30',
        "WARN"     : '30',
        "INFO"     : '20',
        "DEBUG"    : '10',
        "NOTSET"   : '0'
    }

    if level.upper() in list(LOG_LEVELS.keys()):
        logger.setLevel(int(LOG_LEVELS[level]))
        return logger

    logger.setLevel(20)
    return logger
