# -*- coding: utf-8 -*-
from __future__ import (print_function, division, absolute_import, unicode_literals, )


class VariantType(object):

    def __init__(self, v):
        self.value = v

    def __repr__(self):
        return '{0}: < {1} >'.format(self.__class__.__name__, repr(self.value))

    def bind(self, a_to_m_b):
        raise NotImplementedError

    def map(self, a_b):
        raise NotImplementedError

    def __rshift__(self, a_to_m_b):
        ''' >> '''
        return self.bind(a_to_m_b)
