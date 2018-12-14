__author__ = 'victor'

import logging

_LOG_LEVEL = logging.ERROR

def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(_LOG_LEVEL)
    # # create file handler which logs even debug messages
    # fh = logging.FileHandler('spam.log')
    # fh.setLevel(logging.DEBUG)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(_LOG_LEVEL)
    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # add the handlers to the logger
    # logger.addHandler(fh)
    logger.addHandler(ch)

    return logger
