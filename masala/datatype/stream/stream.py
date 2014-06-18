# -*- coding: utf-8 -*-
from __future__ import (print_function, division, absolute_import, unicode_literals, )

from ..base import VariantType
from ...utils import compose
from ...shorthand import MethodComposer
from .error import (
    NoContentStreamError,
    LessContentStreamError,
    NotIterableError,
)


class Stream(VariantType):
    __slots__ = ('value', 'xs', )

    def __init__(self, xs=None):
        self.xs = xs
        super(Stream, self).__init__(lambda ys: ys)

    def bind(self, l_T_to_l_U):
        return compose(self.value, l_T_to_l_U)

    def map(self, l_T_to_l_U):
        self.value = compose(self.value, l_T_to_l_U)
        return self

    def __lshift__(self, xs):
        self.xs = self.value(xs)
        self.value = lambda ys: ys
        return self

    def __iter__(self):
        return iter(self.value(self.xs))

    def evaluate(self, xs=None):
        if self.xs and xs:
            raise TypeError('Too many arguments')

        try:
            if self.xs:
                return self.value(self.xs)
            return self.value(xs)
        except TypeError as e:
            return Empty(NotIterableError(e.message))


class Empty(Stream):
    __slots__ = ('value', 'xs', 'error', )

    def __init__(self, error=None):
        self.error = error
        super(Stream, self).__init__(None)

    def map(self, l_T_to_l_U):
        return self

    def __lshift__(self, xs):
        return self

    def __call__(self, xs=None):
        return self

    def __repr__(self):
        return super(Stream, self).__repr__() + " reason => " + str(type(self.error))


# class OrderedStream(Stream):
#     def __init__(self, xs, key_from_x):
#         self.xs = xs
#         self.key_from_x = key_from_x
#         return
#
#     def __iter__(self):
#         xsd = self.xs | to_list()
#         xsd.sort(key = self.key_from_x)
#         for x in xsd:
#             yield x
#
#


def _method_composer_to_callable(x):
    if isinstance(x, MethodComposer):
        return x.fin__()
    return x



def dispatch_stream(original_query):
    '''
    decorator to dispatch the function should be chaining method of masala.Stream

    :type original_query: AnyObjects -> iter
    '''
    func_name = original_query.func_name

    # TODO: should be methodtype?
    # TODO: should support MethodComposer?
    def _method_chaining_base(self, *args, **kw):
        return self.map(
            lambda xs: original_query(
                xs,
                *[_method_composer_to_callable(a) for a in args],
                **kw
            )
        )
    setattr(Stream, func_name, _method_chaining_base)


def endpoint_of_stream(original_query):
    '''
    decorator to dispatch the function should be end of chaining method of masala.Stream

    :type original_query: AnyObjects -> T
    '''
    func_name = original_query.func_name

    # TODO: should be methodtype?
    # TODO: should support MethodComposer?
    def _evaluatable_method(self, *args, **kw):
        return self.map(lambda xs: original_query(xs, *args, **kw)).evaluate()
    setattr(Stream, func_name, _evaluatable_method)
