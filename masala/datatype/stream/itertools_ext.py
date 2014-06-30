# -*- coding: utf-8 -*-

'''
itertools_ext - itertools port for method of masala.Stream
Copyright (C) 2014 OGURA_Daiki <https://github.com/hachibeeDI>
License: So-called MIT/X license
    Permission is hereby granted, free of charge, to any person
    obtaining a copy of this software and associated documentation
    files (the "Software"), to deal in the Software without
    restriction, including without limitation the rights to use,
    copy, modify, merge, publish, distribute, sublicense, and/or
    sell copies of the Software, and to permit persons to whom the
    Software is furnished to do so, subject to the following
    conditions:

    The above copyright notice and this permission notice shall be
    included in all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
    EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
    OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
    NONINFRINGEMENT.  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
    HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
    WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
    FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
    OTHER DEALINGS IN THE SOFTWARE.

    And some ideas inspired by https://github.com/kana/py-llll
    created by Kana Natsuno <http://whileimautomaton.net/>
'''


from __future__ import (print_function, division, absolute_import, unicode_literals, )

import operator

from six.moves import reduce as iter_reduce
import six.moves.builtins as __builtins__  # not __builtin__

from six import PY2
if PY2:
    from itertools import (
        ifilterfalse as iter_filterfalse,
        izip as iter_zip,
        imap as iter_map,
        ifilter as iter_filter,
    )

    def iter_accumulate(iterable, func=operator.add):
        it = iter(iterable)
        total = next(it)
        yield total
        for element in it:
            total = func(total, element)
            yield total
else:
    from itertools import (
        filterfalse as iter_filterfalse,
        accumulate as iter_accumulate,
    )
    iter_map = map
    iter_filter = filter
    iter_zip = zip


from .stream import (
    Empty,
    dispatch_stream,
    endpoint_of_stream,
)
# from .error import (
#     NoContentStreamError,
#     LessContentStreamError,
#     NotIterableError,
# )


@endpoint_of_stream
def to_list(xs):
    return list(xs)


@dispatch_stream
def map_(xs, x_to_y):
    return iter_map(x_to_y, xs)


@dispatch_stream
def filter(xs, predicate):
    return iter_filter(predicate, xs)


@dispatch_stream
def filterfalse(xs, predicate):
    return iter_filterfalse(predicate, xs)


@dispatch_stream
def accumulate(xs, predicate=operator.add):
    return iter_accumulate(xs, predicate)


@endpoint_of_stream
def reduce(xs, func, initializer=None):
    if initializer:
        return iter_reduce(func, xs, initializer)
    else:
        return iter_reduce(func, xs)


@dispatch_stream
def chain(xs, *yzs):
    return chain(xs, *yzs)


@dispatch_stream
def slice(xs, *args):
    from itertools import islice
    return islice(xs, *args)


@dispatch_stream
def takewhile(xs, predicate):
    from itertools import takewhile as iter_takewhile
    return iter_takewhile(predicate, xs)


@dispatch_stream
def dropwhile(xs, predicate):
    from itertools import dropwhile as iter_dropwhile
    return iter_dropwhile(predicate, xs)


@dispatch_stream
def groupby(xs, key=None):
    from itertools import iter_groupby
    return iter_groupby(xs, key)


@endpoint_of_stream
def all(xs, predicate=None):
    print(xs)
    print(predicate)
    if predicate:
        return __builtins__.all(x for x in xs if predicate(x))
    else:
        return __builtins__.all(xs)


@endpoint_of_stream
def any(xs, predicate=None):
    # print(xs)
    # print(predicate)
    if predicate:
        return __builtins__.any(x for x in xs if predicate(x))
    else:
        return __builtins__.any(xs)
