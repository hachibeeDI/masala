# -*- coding: utf-8 -*-
from __future__ import (print_function, division, absolute_import, unicode_literals, )


def flip(f):
    return lambda x, y: f(y, x)


def expr(x):
    return lambda: x


def identity(x):
    return x


def constant(x, y):
    return x


# @infix
def compose(f_t_u, f_u_r):
    return lambda t: f_u_r(f_t_u(t))


class _Apply(object):
    def __rlshift__(self, other):
        self.value = other
        return self

    def __rshift__(self, other):
        return other(self.value)
apply = _Apply()
