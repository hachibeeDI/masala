
# Masala

## ex

### curry

```python

>>> from masala import CurryContainer as cc
>>> cur = cc(lambda a, b, c: [a, b, c])
>>> _ = cur << 'aaa' << 'bbb'
>>> cur('ccc')
['aaa', 'bbb', 'ccc']
>>> cur = cc(lambda a, b='hogeeee', c='foooo': [a, b, c])
>>> _ = cur << 'a' << ('c', 'c')
>>> cur('b')
['a', 'b', 'c']

>>> from masala import curried
>>> @curried
... def sum5(a, b, c, d, e):
...     return a + b + c + d + e
...
>>> sum0 = sum5 << 1 << 2 << 3 << 4 << 5
>>> sum0.call()  # same as sum0()
15

```


### lambda

```python

>>> from masala.result import Either
>>> from masala import lambd as _
>>> Either.right('hachi') >> _.title()
'Hachi'
>>> replacer = _.replace(_, _)
>>> replacer('hachi', 'chi', 'chiboee')
'hachiboee'
>>> map(_ + 2, range(3))
[2, 3, 4]
>>> reduce(_ + _, range(5))
10

```

### method chaining

```python

>>> from masala import Builder as _
>>> Either.right('hachi') >> _.method.title().replace('i', 'U').replace('c', 'z').fin__()
'HazhU'
>>> Either.right(4) >> ((_.m + 4) * 'py'.title()).fin__()
'PyPyPyPyPyPyPyPy'
>>> (_.met + 1 + 2 + 3 + 4 + 5).apply__(0)
15

```


### Pattern Match


```python

>>> from masala import Match

>>> match = Match(10)
>>> if match.when(1):
...    print 'boo'
... elif match.when(10):
...    print 'yieeeee'
yieeeee


>>> from masala import Wildcard as _

>>> match = Match([1, 2, 3])
>>> @match.when([2, 2, 2], let_=('one', 'two', 'thr'))
... def case1(one, two, thr):
...     print one, two, thr
...     return one
>>> @match.when([_, 2, 3], let_=('one', '_', 'thr'))
... def case2(one, thr):
...    print 'one: {0} two: {1} thr: {2}'.format(one, '_', thr)
...    return one
one: 1 two: _ thr: 3
>>> assert match.end == 1

>>> match = Match('python')
>>> @match.when(_.isdigit(), let_='moo')
... def case1(moo):
...     print one, two, thr
...     return one
>>> @match.when(_ == 'python', let_=('a'))
... def case2(a):
...     return a
>>> assert match.end == 'python'

```
