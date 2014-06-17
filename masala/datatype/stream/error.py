# -*- coding: utf-8 -*-
from __future__ import (print_function, division, absolute_import, unicode_literals, )


class NoContentStreamError(Exception):
    pass


class LessContentStreamError(Exception):
    pass


class NotIterableError(Exception):
    pass
