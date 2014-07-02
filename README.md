
# Masala

master: [![Build Status](https://travis-ci.org/hachibeeDI/masala.svg?branch=master)](https://travis-ci.org/hachibeeDI/masala)

## ex

### curry

```python

>>> from __future__ import (print_function, division, absolute_import, unicode_literals, )
>>> from masala import CurryContainer as cc
>>> cur = cc(lambda a, b, c: [a, b, c])
>>> cur = cur << 'aaa' << 'bbb'
>>> cur('ccc')
['aaa', 'bbb', 'ccc']

>>> cur = cc(lambda a, b='hogeeee', c='foooo': [a, b, c])
>>> cur = cur << 'a' << ('c', 'c')
>>> cur('b')
['a', 'b', 'c']

>>> from masala import curried
>>> @curried
... def sum5(a, b, c, d, e):
...     return a + b + c + d + e
...
>>> sum0 = sum5 << 1 << 2 << 3 << 4 << 5
>>> assert sum0() == sum5(1, 2, 3, 4, 5)

```


### lambda

```python

>>> from masala import lambd as _
>>> from masala.datatype import Either
>>> Either.right('hachi') >> _.title()
'Hachi'
>>> replacer = _.replace(_, _)
>>> replacer('hachi', 'chi', 'chiboee')
'hachiboee'
>>> list(map(_ + 2, range(3)))
[2, 3, 4]
>>> from six.moves import reduce
>>> reduce(_ + _, range(5))
10

```

### method chaining

```python

>>> from masala import BuilderAllowsMethodChaining as __
>>> Either.right('hachi') >> __.title().replace('i', 'U').replace('c', 'z')
'HazhU'
>>> foolambda = __.title().replace('i', 'U').replace('c', 'z')
>>> foolambda('hachi')
'HazhU'

>>> Either.right(4) >> ((__ + 4) * 'py'.title())
'PyPyPyPyPyPyPyPy'
>>> (__ + 1 + 2 + 3 + 4 + 5)(0)
15
>>> (__ + 1 + 2 + 3 + 4 + 5).apply__(0)
15

```

### list processing

```python

>>> from masala import (apply as a, lambd as _, )
>>> from masala.datatype import Stream
>>> # extends linq like methods to Stream.
>>> # but I reccomend to use itertools extention is also prepared as `from masala.datatype.stream import itertools_ext`
>>> from masala.datatype.stream import linq_ext
>>> Stream([1, 2, 3]).select(_ * 2).to_list()
[2, 4, 6]
>>> # support lazy evaluation
>>> Stream([1, 2, 3]).select(_ * 2)  # doctest:+ELLIPSIS
Stream: < <function ...

>>> Stream(range(0, 15)).select(_ + 1).where(__ % 2 == 0).to_list()
[2, 4, 6, 8, 10, 12, 14]

>>> Stream(range(0, 100)).select(_ * 2).where(_ > 1000).first()  # doctest:+ELLIPSIS
Empty: < None > reason => <class 'masala.datatype.stream.error.NoContentStreamError'>:

>>> Stream(range(0, 100)).select(_ * 2).any(_ > 1000)
False
>>> Stream(111111).select(_ * 2).to_list()
Empty: < None > reason => <class 'masala.datatype.stream.error.NotIterableError'>: 'int' object is not iterable

>>> # you can extend the method by yourself
>>> from masala.datatype.stream import dispatch_stream
>>> @dispatch_stream
... def my_select(xs, x_to_y):
...     for x in xs:
...         yield x_to_y(x)
>>> Stream([1, 2, 3]).my_select(_ * 2).to_list()
[2, 4, 6]
>>> from masala.datatype.stream import delete_dispatchedmethods
>>> # you can clean extentions.
>>> delete_dispatchedmethods(['my_select'])

>>> # other cases
>>> twicer = Stream().select(_ * 2)
>>> twiced = twicer << [1, 2, 3]
>>> list(twiced)
[2, 4, 6]
>>> twiced2 = twicer << [2, 3, 4]
>>> list(twiced2)
[4, 6, 8]

>>> delete_dispatchedmethods(linq_ext.__all__)

```


### Pattern Match


```python

>>> from masala import Match

>>> match = Match(10)
>>> if match.when(1):
...    print('boo')
... elif match.when(10):
...    print('yieeeee')
yieeeee


>>> from masala import Wildcard as _

>>> match = Match([1, 2, 3])
>>> @match.when([2, 2, 2], let_=('one', 'two', 'thr'))
... def case1(one, two, thr):
...     return 'case1'
>>> @match.when([_, 2, 3], let_=('one', '_', 'thr'))
... def case2(one, thr):
...    return 'case2'
>>> assert match.end == 'case2'

>>> match = Match('python')
>>> @match.when(_.isdigit(), let_='moo')
... def case1(moo):
...     return one
>>> @match.when(_ == 'python', let_=('a'))
... def case2(a):
...     return a
>>> assert match.end == 'python'

```


### call method with optional values

```python

>>> from masala import Perhaps

>>> p = Perhaps('hoge huga foo')
>>> p.try_('replace', 'huga', 'muoo').try_('upper').get()
'HOGE MUOO FOO'
>>> p.apply(len).get()
13

>>> nonecase = Perhaps(None).try_('replace', 'huga', 'muoo').try_('upper')
>>> nonecase.get()

>>> nonecase.get_or('nnnnn')
'nnnnn'

```


## Support

tested version of Python is

- 2.7
- 3.4
