# -*- coding: utf-8 -*-
from __future__ import (print_function, division, absolute_import, unicode_literals, )

from logging import (
    StreamHandler,
    Formatter,
    getLogger,
    DEBUG,
    INFO,
)

MasalaHandler = StreamHandler()
MasalaHandler.setFormatter(Formatter("%(levelname)s: [in %(name)s : %(funcName)s] '%(message)s'"))
MasalaHandler.setLevel(INFO)


def get_root_logger(level=DEBUG):
    logger = getLogger('masala')
    logger.addHandler(MasalaHandler)
    logger.setLevel(level)
    return logger


def get_logger(name, level=DEBUG):
    '''
    Usage:

    >>> logger = get_logger(__name__)
    '''
    logger = getLogger(name)
    logger.setLevel(level)
    return logger


def set_debug_level(level):
    MasalaHandler.setLevel(level)


def as_debug_mode():
    set_debug_level(DEBUG)
