# -*- coding: utf-8 -*-
from __future__ import (print_function, division, absolute_import, unicode_literals, )

from operator import methodcaller


class Perhaps(object):

    def __init__(self, var):
        self.var = var

    def try_(self, methodname, *args, **kw):
        v = self.var
        if v is None:
            return self
        else:
            self.var = methodcaller(methodname, *args, **kw)(v)
            return self

    def apply(self, func, *args, **kw):
        v = self.var
        if v is None:
            return self
        else:
            self.var = func(self.var, *args, **kw)
            return self

    def get(self):
        return self.var

    def get_or(self, val):
        if self.var:
            return self.var
        else:
            return val

    def __nonzero__(self):
        return self.var
