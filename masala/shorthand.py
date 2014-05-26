# -*- coding: utf-8 -*-
from __future__ import (print_function, division, absolute_import, unicode_literals, )

import operator
from sys import version_info

from .utils import (
    compose,
)


class Builder(object):

    def __init__(self): pass

    def __getattr__(self, name):
        if name in ('lambd', 'lam', 'l'):
            return LambdaBuilder
        elif name in ('method', 'met', 'm'):
            return MethodComposer()
        else:
            raise AttributeError()
Builder = Builder()


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


def _composing_operation_builder(op, doc):
    def _dummy_method(dummy_self, other):
        dummy_self.chains.append(lambda *a, **kw: lambda trueself: op(trueself, other))
        dummy_self.args.append(((other,), {}, ))
        return dummy_self
    return _dummy_method


class MethodComposer(object):
    __slots__ = ('chains', 'args', )

    def __init__(self):
        self.chains = []
        self.args = []

    def __getattr__(self, name):
        self.chains.append(_methodbuilder(name))
        return self.__compose

    def __compose(self, *a, **kw):
        self.args.append((a, kw))
        return self

    def fin__(self):
        methods = [x(*y[0], **y[1]) for x, y in zip(self.chains, self.args)]
        return reduce(compose, methods)

    def apply__(self, var):
        return self.fin__()(var)


    __add__ = _composing_operation_builder(operator.add, "self + other")
    __mul__ = _composing_operation_builder(operator.mul, "self * other")
    __sub__ = _composing_operation_builder(operator.sub, "self - other")
    __mod__ = _composing_operation_builder(operator.mod, "self %% other")
    __pow__ = _composing_operation_builder(operator.pow, "self ** other")

    __and__ = _composing_operation_builder(operator.and_, "self & other")
    __or__ = _composing_operation_builder(operator.or_, "self | other")
    __xor__ = _composing_operation_builder(operator.xor, "self ^ other")

    if version_info[0] == 2:
        __div__ = _composing_operation_builder(operator.div, "self / other")
    else:
        __div__ = _composing_operation_builder(operator.truediv, "self / other")
    __divmod__ = _composing_operation_builder(divmod, "self / other")
    __floordiv__ = _composing_operation_builder(operator.floordiv, "self / other")
    __truediv__ = _composing_operation_builder(operator.truediv, "self / other")

    __lshift__ = _composing_operation_builder(operator.lshift, "self << other")
    __rshift__ = _composing_operation_builder(operator.rshift, "self >> other")

    __lt__ = _composing_operation_builder(operator.lt, "self < other")
    __le__ = _composing_operation_builder(operator.le, "self <= other")
    __gt__ = _composing_operation_builder(operator.gt, "self > other")
    __ge__ = _composing_operation_builder(operator.ge, "self >= other")
    __eq__ = _composing_operation_builder(operator.eq, "self == other")
    __ne__ = _composing_operation_builder(operator.ne, "self != other")


if __name__ == '__main__':
    import doctest
    doctest.testmod()
