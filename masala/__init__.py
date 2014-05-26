# -*- coding: utf-8 -*-
from __future__ import (print_function, division, absolute_import, unicode_literals, )

import types

from .shorthand import Builder
from .utils import (
    expr,
    flip,
    identity,
    constant,
    compose,
)


class CurryContainer(object):
    '''
    >>> cur = CurryContainer(lambda a, b, c: print([a, b, c]))
    >>> _ = cur << 'aaa' << 'bbb'
    >>> cur('ccc')
    [u'aaa', u'bbb', u'ccc']
    >>> cur = CurryContainer(lambda a, b='hogeeee', c='foooo': print([a, b, c]))
    >>> _ = cur << 'a' << ('c', 'c')
    >>> cur('b')
    [u'a', u'b', u'c']
    '''

    __slots__ = ('func', 'args', 'argkw', )

    def __init__(self, func):
        self.func = func
        self.args = []
        self.argkw = []

    def __push_arg(self, arg):
        if isinstance(arg, types.TupleType):
            self.argkw.append(arg)
        else:
            self.args.append(arg)

    def __lshift__(self, arg):
        self.__push_arg(arg)
        return self

    def __call__(self, arg=None):
        if arg:
            self.__push_arg(arg)
        return self.func(*self.args, **dict(self.argkw))


if __name__ == '__main__':
    import doctest
    doctest.testmod()
