
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

```


### lambda

```python

>>> from masala.result import Either
>>> from masala import Builder as _
>>> Either.right('hachi') >> _.lambd.title()
'Hachi'
>>> map(_.l + 2, range(3))
[2, 3, 4]

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
