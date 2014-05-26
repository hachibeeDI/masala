# -*- coding: utf-8 -*-
from __future__ import (print_function, division, absolute_import, unicode_literals, )

import types
import operator
from sys import version_info


flip = lambda f: lambda x, y: f(y, x)


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


def _methodbuilder(name):
    return lambda *args, **kw: operator.methodcaller(name, *args, **kw)


def _opp_builder(op, doc):
    def _dummy_method(dummy_self, other):
        return lambda trueself: op(trueself, other)
    return _dummy_method


class LambdaBuilder(object):
    '''
    >>> from result import Either
    >>> Either.right('hachi') >> _.title()
    u'Hachi'
    >>> map(_ + 2, range(3))
    [2, 3, 4]
    >>> Either.right(print) >> _('hello world!')
    hello world!
    '''
    __slots__ = ()

    @classmethod
    def __getattr__(self, name):
        return _methodbuilder(name)

    def __call__(self, *args, **kw):
        return lambda func: func(*args, **kw)

    # TODO: implement all operators
    __add__ = _opp_builder(operator.add, "self + other")
    __mul__ = _opp_builder(operator.mul, "self * other")
    __sub__ = _opp_builder(operator.sub, "self - other")
    __mod__ = _opp_builder(operator.mod, "self %% other")
    __pow__ = _opp_builder(operator.pow, "self ** other")

    __and__ = _opp_builder(operator.and_, "self & other")
    __or__ = _opp_builder(operator.or_, "self | other")
    __xor__ = _opp_builder(operator.xor, "self ^ other")

    if version_info[0] == 2:
        __div__ = _opp_builder(operator.div, "self / other")
    else:
        __div__ = _opp_builder(operator.truediv, "self / other")
    __divmod__ = _opp_builder(divmod, "self / other")
    __floordiv__ = _opp_builder(operator.floordiv, "self / other")
    __truediv__ = _opp_builder(operator.truediv, "self / other")

    __lshift__ = _opp_builder(operator.lshift, "self << other")
    __rshift__ = _opp_builder(operator.rshift, "self >> other")

    __lt__ = _opp_builder(operator.lt, "self < other")
    __le__ = _opp_builder(operator.le, "self <= other")
    __gt__ = _opp_builder(operator.gt, "self > other")
    __ge__ = _opp_builder(operator.ge, "self >= other")
    __eq__ = _opp_builder(operator.eq, "self == other")
    __ne__ = _opp_builder(operator.ne, "self != other")


LambdaBuilder = LambdaBuilder()


if __name__ == '__main__':
    import doctest
    doctest.testmod()
