
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
>>> from masala import Builder as _
>>> Either.right('hachi') >> _.lambd.title()
'Hachi'
>>> replacer = _.lambd.replace(_, _)
>>> replacer('hachi', 'chi', 'chiboee')
'hachiboee'
>>> map(_.l + 2, range(3))
[2, 3, 4]
>>> reduce(_.l + _, range(5))
10

```

```python

>>> from masala import Builder as _
>>> Either.right('hachi') >> _.method.title().replace('i', 'U').replace('c', 'z').fin__()
'HazhU'
>>> Either.right(4) >> ((_.m + 4) * 'py'.title()).fin__()
'PyPyPyPyPyPyPyPy'
>>> (_.met + 1 + 2 + 3 + 4 + 5).apply__(0)
15

```
