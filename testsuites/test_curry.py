import unittest

from masala import CurryContainer as cc
from masala import curried


class TestCurryContainer(unittest.TestCase):
    def test_basic(self):
        cur = cc(lambda a, b, c: [a, b, c])
        cur = cur << 'aaa' << 'bbb'
        self.assertEqual(cur('ccc'), ['aaa', 'bbb', 'ccc'])

    def test_named_args(self):
        cur = cc(lambda a, b='hogeeee', c='foooo': [a, b, c])
        cur = cur << 'a' << ('c', 'c')
        self.assertEqual(cur(b='boee'), ['a', 'boee', 'c'])

    def test_decotator(self):

        @curried
        def sum5(a, b, c, d, e):
            return a + b + c + d + e
        sum0 = sum5 << 1 << 2 << 3 << 4 << 5
        self.assertEqual(sum0(), sum5(1, 2, 3, 4, 5))

    def test_overargs(self):
        @curried
        def emp(a):
            return a
        with self.assertRaises(TypeError):
            a_emp = emp << 'a'
            a_emp(1, 2, 3)
