# -*- coding: utf-8 -*-
from __future__ import (print_function, division, absolute_import, unicode_literals, )

from six import PY2
from six.moves import reduce

import operator
from itertools import chain

from .utils import (
    compose,
)


def _append_operator_ploxy(name):
    def _operator(self, other):
        m = MethodComposer()
        return getattr(m, name)(other)
    return _operator


class BuilderAllowsMethodChaining(object):
    ''' ploxy to construct MethodComposer
    '''

    def __init__(self): pass

    def __getattr__(self, name):
        return getattr(MethodComposer(), name)

    __add__ = _append_operator_ploxy('__add__')
    __mul__ = _append_operator_ploxy('__mul__')
    __sub__ = _append_operator_ploxy('__sub__')
    __mod__ = _append_operator_ploxy('__mod__')
    __pow__ = _append_operator_ploxy('__pow__')

    __and__ = _append_operator_ploxy('__and__')
    __or__ = _append_operator_ploxy('__or__')
    __xor__ = _append_operator_ploxy('__xor__')

    if PY2:
        __div__ = _append_operator_ploxy('__div__')
    else:
        __div__ = _append_operator_ploxy('__div__')
    __divmod__ = _append_operator_ploxy('__divmod__')
    __floordiv__ = _append_operator_ploxy('__floordiv__')
    __truediv__ = _append_operator_ploxy('__truediv__')

    __lshift__ = _append_operator_ploxy('__lshift__')
    __rshift__ = _append_operator_ploxy('__rshift__')

    __lt__ = _append_operator_ploxy('__lt__')
    __le__ = _append_operator_ploxy('__le__')
    __gt__ = _append_operator_ploxy('__gt__')
    __ge__ = _append_operator_ploxy('__ge__')
    __eq__ = _append_operator_ploxy('__eq__')
    __ne__ = _append_operator_ploxy('__ne__')
BuilderAllowsMethodChaining = BuilderAllowsMethodChaining()


def _does_arguments_has_placeholder(arg):
    '''
    ATTENTION: use Builders as placeholder
    '''
    return isinstance(arg, (BuilderAllowsMethodChaining.__class__, LambdaBuilder.__class__, MethodComposer, ))


def _methodbuilder(name):
    def _(*a, **kw):
        all_args = chain(a, kw.values())
        num_of_placeholder = sum(1 for arg in all_args if _does_arguments_has_placeholder(arg))
        if not num_of_placeholder:
            return operator.methodcaller(name, *a, **kw)
        a = list(a)
        for i in range(num_of_placeholder):
            a.pop(0)
        # TODO: meta level generation
        if num_of_placeholder == 1:
            return lambda self, a1: operator.methodcaller(name, a1, *a, **kw)(self)
        elif num_of_placeholder == 2:
            return lambda self, a1, a2: operator.methodcaller(name, a1, a2, *a, **kw)(self)
        elif num_of_placeholder == 3:
            return lambda self, a1, a2, a3: operator.methodcaller(name, a1, a2, a3, *a, **kw)(self)
        else:
            raise NotImplementedError('not max len of placeholder is 3 yet')
    return _


def _opp_builder(op, doc):
    def _dummy_method(dummy_self, other):
        if isinstance(other, (BuilderAllowsMethodChaining.__class__, LambdaBuilder.__class__, MethodComposer, )):
            return lambda trueself, trueother: op(trueself, trueother)
        else:
            return lambda trueself: op(trueself, other)
    return _dummy_method


class LambdaBuilder(object):
    '''
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

    if PY2:
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

    def __call__(self, *args, **kw):
        ''' to use same as lambda.
            but this is not became callable
        '''
        func = self.fin__()
        return func(*args, **kw)

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

    if PY2:
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
