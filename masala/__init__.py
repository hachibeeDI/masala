# -*- coding: utf-8 -*-
from __future__ import (print_function, division, absolute_import, unicode_literals, )

from masala.logging import (
    get_root_logger,
)
_logger = get_root_logger()


from inspect import getargspec

from .shorthand import BuilderAllowsMethodChaining, LambdaBuilder
lambd = LambdaBuilder
from .match import Match, Wildcard
from .perhaps import Perhaps
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

    __slots__ = ('func', )

    def __init__(self, func):
        self.func = func

    def __lshift__(self, arg):
        content = CurriedContent(self.func)
        content._push_arg(arg)
        return content

    def __call__(self, *args, **kw):
        return self.func(*args, **kw)


class CurriedContent(object):
    __slots__ = ('func', 'args', 'argkw', )

    def __init__(self, func):
        self.func = func
        self.args = []
        self.argkw = []

    def _push_arg(self, arg):
        if isinstance(arg, tuple):
            self.argkw.append(arg)
        else:
            self.args.append(arg)

    def __lshift__(self, arg):
        self._push_arg(arg)
        return self

    def __call__(self, *args, **kw):
        argslen = len(self.args + self.argkw) + len(args) + len(kw)
        maxarglen = len(getargspec(self.func).args)
        if maxarglen < argslen:
            raise TypeError('{0} takes at most {1} argument ({2} given)'.format(
                self.func.__name__, maxarglen, argslen))

        args_for_deliver = self.args
        if args:
            args_for_deliver.extend(args)
        kw_for_deliver = dict(self.argkw)
        if kw:
            kw_for_deliver.update(kw)
        return self.func(*args_for_deliver, **kw_for_deliver)


curried = CurryContainer


if __name__ == '__main__':
    import doctest
    doctest.testmod()
