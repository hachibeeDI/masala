# -*- coding: utf-8 -*-
from __future__ import (print_function, division, absolute_import, unicode_literals, )

from .base import VariantType


class Either(VariantType):
    @classmethod
    def right(cls, var=None):
        return Right(var)

    @classmethod
    def left(cls, var=None):
        return Left(var)

    def __nonzero__(self):
        return self.is_right()

    def is_left(self):
        return self.__class__.__name__ == 'Left'

    def is_right(self):
        return self.__class__.__name__ == 'Right'

    def match(self, right, left):
        mytype = self.__class__.__name__
        if mytype == 'Right':
            return right(self.value)
        elif mytype == 'Left':
            return left(self.value)
        else:
            assert False, 'Unexpected value'


class Left(Either):
    def bind(self, a_to_m_b):
        return self

    def map(self, a_b):
        return self

    def __eq__(self, other):
        return isinstance(other, Left)


class Right(Either):
    def bind(self, a_to_m_b):
        return a_to_m_b(self.value)

    def map(self, a_b):
        return self

    def __eq__(self, other):
        if not isinstance(other, Right):
            return False
        return self.value == other.value
