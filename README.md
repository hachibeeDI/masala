
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
>>> from masala import LambdaBuilder as _
>>> Either.right('hachi') >> _.title()
'Hachi'
>>> map(_ + 2, range(3))
[2, 3, 4]

```
