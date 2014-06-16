# -*- coding:utf-8 -*-

from types import (
    TupleType,
    ListType,
    DictionaryType,
)

from six import (iteritems, add_metaclass, )

from masala.shorthand import MethodComposer


class _EqualedMimic(object):
    ''' boolean評価ではTrueを返しつつ、MethodComposerへのプロキシとしても動く '''

    def __init__(self, mimic):
        self.mimic = mimic

    def __nonzero__(self):
        return True

    def __getattr__(self, name):
        return getattr(self.mimic, name)


class _Wildcard(object):
    def __eq__(self, other):
        return MethodComposer() == other
        return True

    def __getattr__(self, name):
        return getattr(MethodComposer(), name)
Wildcard = _Wildcard()


def _is_match(var, target, let_, expr):
    # TODO: clean up
    if _is_match_as_lambda_mimic(var, target):
        try:
            if target.fin__()(var):
                return MatchedLambdaMimic(match_expr=expr, binder=let_)
            else:
                return NotMatched
        except AttributeError:
            return NotMatched


    if _is_match_as_iterable(var, target):
        return MatchedAsIterable(match_expr=expr, binder=let_)
    if _is_match_as_dict(var, target):
        return MatchedAsDictionary(match_expr=expr, binder=let_)
    if var == target:
        return MatchedResult(expr, let_)
    return NotMatched


def _is_match_as_lambda_mimic(var, targ):
    return isinstance(targ, MethodComposer)


def _is_match_as_iterable(var, targ):
    '''
    list, tuple とマッチ. dict, generatorは無視
    '''
    if not (isinstance(var, (TupleType, ListType, ), ) or isinstance(targ, (TupleType, ListType, ), )):
        return False
    # めんどいので単純な比較
    return tuple(var) == tuple(targ)


def _is_match_as_dict(var, targ):
    ''' '''
    if not (isinstance(var, DictionaryType) and isinstance(targ, DictionaryType)):
        return False
    return var == targ


class MatchedResult(object):
    def __init__(self, match_expr, binder):
        self.match_expr = match_expr
        self.binder = binder

    def __call__(self, func):
        self.match_expr._match_result_holder = func()
        del func


class MatchedAsIterable(MatchedResult):
    def __call__(self, func):
        kw = {k: v for k, v in zip(self.binder, self.match_expr.value) if not k == '_'}
        self.match_expr._match_result_holder = func(**kw)
        del func


class MatchedAsDictionary(MatchedResult):
    def __call__(self, func):
        kw = {k: v for k, v in zip(self.binder, iteritems(self.match_expr.value)) if not k == '_'}
        self.match_expr._match_result_holder = func(**kw)
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
        cls.__class__.__nonzero__ = new__nonzero__


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
        is_equals = _is_match(self.value, target, let_, expr=self)
        self._already_matched = is_equals is not NotMatched
        return is_equals

    def __repr__(self):
        return str(self.__dict__)

    @property
    def end(self):
        return self._match_result_holder
