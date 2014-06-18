# -*- coding: utf-8 -*-
from __future__ import (print_function, division, absolute_import, unicode_literals, )

import types
from inspect import getargspec

from .shorthand import BuilderAllowsMethodChaining, LambdaBuilder
lambd = LambdaBuilder
from .match import Match, Wildcard
from .utils import (
    expr,
    flip,
    identity,
    constant,
    compose,
    apply,
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

    __slots__ = ('func', 'maxarglen', 'args', 'argkw', )

    def __init__(self, func):
        self.func = func
        self.maxarglen = len(getargspec(func).args)
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
        argslen = len(self.args + self.argkw) + bool(arg is not None)
        if self.maxarglen < argslen:
            raise TypeError('{0} takes at most {1} argument ({2} given)'.format(
                self.func.__name__, self.maxarglen, argslen))
        if arg:
            self.__push_arg(arg)
        return self.func(*self.args, **dict(self.argkw))

    def call(self, arg=None):
        return self.__call__(arg)


curried = CurryContainer


if __name__ == '__main__':
    import doctest
    doctest.testmod()
