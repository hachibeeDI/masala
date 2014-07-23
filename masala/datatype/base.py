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

    def __match__(self, other):
        from inspect import getmro
        # TODO: should refactor with single dispatch?
        if isinstance(other, type):
            if VariantType in getmro(other):
                return type(self) == other
            else:
                return False

        if isinstance(other, VariantType):
            if type(self) == type(other):
                return self.value == other.value
        else:
            return self.value == other

        return False

    def __evalucate_matches__(self, func):
        return func(self.value, )
