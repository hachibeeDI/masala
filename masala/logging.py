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
MasalaHandler.setFormatter(Formatter("%(levelname)s: [in %(funcName)s] '%(message)s'"))
MasalaHandler.setLevel(INFO)


def get_logger(name, level=DEBUG):
    '''
    Usage:

    >>> logger = get_logger(__name__)
    '''
    logger = getLogger(name)
    logger.setLevel(level)
    logger.addHandler(MasalaHandler)
    return logger


def as_debug_mode():
    MasalaHandler.setLevel(DEBUG)
