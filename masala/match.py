# -*- coding:utf-8 -*-


'''
TODO: should be customizable with implements __match__ method
'''


from six import (iteritems, add_metaclass, )

from .shorthand import MethodComposer
from .shorthand import _append_operator_ploxy
from .datatype import VariantType


class _Wildcard(object):
    ''' In a boolean context, this instance always return True.
        On the other hand it is work as ploxy of MethodComposer.
    '''

    def __nonzero__(self):
        return True

    def __bool__(self):
        return True

    def __getattr__(self, name):
        return getattr(MethodComposer(), name)

    __lt__ = _append_operator_ploxy('__lt__')
    __le__ = _append_operator_ploxy('__le__')
    __gt__ = _append_operator_ploxy('__gt__')
    __ge__ = _append_operator_ploxy('__ge__')
    __eq__ = _append_operator_ploxy('__eq__')
    __ne__ = _append_operator_ploxy('__ne__')

Wildcard = _Wildcard()


def _is_match(target, let_, expr):
    var = expr.value
    # TODO: clean up
    if _is_match_as_lambda_mimic(var, target):
        try:
            if target.fin__()(var):
                return MatchedLambdaMimic(match_expr=expr, binder=let_)
            else:
                return NotMatched
        except AttributeError:
            return NotMatched

    if _is_match_as_type_of_variant(var, target):
        return MatchedAsTypeOfVariant(match_expr=expr, binder=None)  # ignore binder
    if _is_match_as_iterable(var, target):
        return MatchedAsIterable(match_expr=expr, binder=let_)
    if _is_match_as_dict(var, target):
        return MatchedAsDictionary(match_expr=expr, binder=let_)
    if var == target:
        return MatchedResult(expr, let_)
    return NotMatched


def _is_match_as_type_of_variant(var, targ):
    ''' passed targ is type of variant, not instance.
    '''
    from inspect import getmro
    if isinstance(targ, type):
        if VariantType not in getmro(targ):
            return False
    return type(var) == targ


def _is_match_as_lambda_mimic(var, targ):
    return isinstance(targ, MethodComposer)


def _is_match_as_iterable(var, targ):
    '''
    list, tuple とマッチ. dict, generatorは無視
    '''
    if not (isinstance(var, (tuple, list, ), ) or isinstance(targ, (tuple, list, ), )):
        return False
    # めんどいので単純な比較
    return tuple(var) == tuple(targ)


def _is_match_as_dict(var, targ):
    ''' '''
    if not (isinstance(var, dict) and isinstance(targ, dict)):
        return False
    return var == targ


class MatchedResult(object):
    def __init__(self, match_expr, binder):
        self.match_expr = match_expr
        self.binder = binder

    def __call__(self, func):
        self.match_expr._match_result_holder = func()
        del func


class MatchedAsTypeOfVariant(MatchedResult):
    def __call__(self, func):
        # type of self.match_expr.value should VariantType
        self.match_expr._match_result_holder = func(self.match_expr.value.value)
        del func


class MatchedAsIterable(MatchedResult):
    def __call__(self, func):
        kw = {k: v for k, v in zip(self.binder, self.match_expr.value) if not k == '_'}
        self.match_expr._match_result_holder = func(**kw)
        del func


class MatchedAsDictionary(MatchedResult):
    def __call__(self, func):
        matched_values = self.match_expr.value
        r = {k: matched_values[k] for k in self.binder if not k == '_'}
        self.match_expr._match_result_holder = func(**r)
        del func


class MatchedLambdaMimic(MatchedResult):
    def __call__(self, func):
        self.match_expr._match_result_holder = func(self.match_expr.value)
        del func



class NonZeroCls(type):
    ''' cls obj should be False in boolean context. '''

    def __init__(cls, name, bases, dct):
        super(NonZeroCls, cls).__init__(name, bases, dct)

        def new__nonzero__(cls):
            return False
        cls.__class__.__nonzero__ = new__nonzero__  # for PY2
        cls.__class__.__bool__ = new__nonzero__  # for PY3


@add_metaclass(NonZeroCls)
class NotMatched(object):
    def __init__(self, *a, **kw):
        pass


class Match(object):

    def __init__(self, value):
        self.value = value
        self._already_matched = False
        self._match_result_holder = None

    def when(self, target, let_=None):
        if self._already_matched:
            return NotMatched
        return self.__match(self.value, target, let_)

    def __match(self, value, target, let_):
        is_equals = _is_match(target, let_, expr=self)
        self._already_matched = is_equals is not NotMatched
        return is_equals

    def __repr__(self):
        return str(self.__dict__)

    @property
    def end(self):
        return self._match_result_holder
