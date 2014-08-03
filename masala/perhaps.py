# -*- coding: utf-8 -*-
from __future__ import (print_function, division, absolute_import, unicode_literals, )

from operator import methodcaller


class _Guard(object):
    def __get__(self, owner, type=None):
        self.owner = owner
        return self

    def __getattr__(self, name):
        owner = self.owner
        if owner.value is None:
            return lambda *_, **__: owner

        def _(*args, **kw):
            owner.value = methodcaller(name, *args, **kw)(owner.value)
            return owner
        return _

    def __eq__(self, other):
        return self.owner.value == other


class Perhaps(object):
    _ = _Guard()

    def __init__(self, value):
        self.value = value

    def __getattr__(self, name):
        def _(*args, **kw):
            self.value = methodcaller(name, *args, **kw)(self.value)
            return self
        return _

    def __rshift__(self, other):
        if self.value is None:
            return self
        self.value = other(self.value)
        return self

    def __repr__(self):
        return repr(self.value)

    def get(self):
        return self.value

    def get_or(self, val):
        if self.value:
            return self.value
        else:
            return val

    def __nonzero__(self):
        return self.value is not None

    def __bool__(self):
        return self.value is not None


if __name__ == '__main__':
    st = Perhaps("hoge")._.upper()._.replace('H', 'n')
    assert st._ == u'nOGE'
    null = Perhaps(None)._.upper()._.replace('H', 'n')
    assert null.get() is None
    assert null.get_or('py') == 'py'
    apply_case = (
        Perhaps(range(10)) >>
        (lambda xs: [x * 2 for x in xs]) >>
        (lambda xs: [x for x in xs if x % 4 == 0]))
    assert apply_case._ == [0,  4,  8,  12,  16]
    assert bool(Perhaps(''))
    assert not bool(Perhaps(None))
