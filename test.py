# -*- coding: utf-8 -*-
from __future__ import (print_function, division, absolute_import, unicode_literals, )

from os import path
CURRENT_DIR = path.dirname(path.abspath(__file__))

import doctest
import unittest
from imp import reload

from masala.datatype import Either

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


from masala import lambd


class TestLambdaBuilder(unittest.TestCase):

    def test_basic(self):
        self.assertEqual(Either.right('hachi') >> lambd.title(), u'Hachi')
        self.assertEqual(list(map(lambd + 2, range(3))), [2, 3, 4])


from masala import Match
from masala import Wildcard as _


class TestMatch(unittest.TestCase):

    def test_ifstatement(self):
        match = Match(10)
        if match.when(1):
            self.assertTrue(False)
        elif match.when(10):
            self.assertTrue(True)

    def test_dummy_block(self):
        match = Match(10)

        @match.when(1)
        def echo1():
            return 'no'

        @match.when(10)
        def truepat():
            return 'iei!'
        self.assertEqual(match.end, 'iei!')

    def test_placeholder_with_dict(self):
        match = Match({'a': 1, 'b': 2})

        @match.when([2, 2, 2], let_=('one', 'two', 'thr'))
        def case1(one, two, thr):
            return one

        @match.when({'a': 1, 'b': _}, let_=('a'))
        def case2(a):
            return a
        self.assertEqual(match.end, 1)

    def test_placeholder_with_methodcalling(self):
        match = Match('python')

        @match.when(_.startwith('aa'), let_='moo')
        def case1(moo):
            return moo

        @match.when(_.startswith('pyt'), let_=('a'))
        def case2(a):
            return a
        self.assertEqual(match.end, 'python')

    def test_placeholder_with_operator(self):
        match = Match('python')

        @match.when(_.isdigit(), let_='moo')
        def case1(moo):
            return moo

        @match.when(_ == 'python', let_=('a'))
        def case2(a):
            return a
        self.assertEqual(match.end, 'python')


from masala.datatype import Right, Left


class TestMatchWithDatatype(unittest.TestCase):

    def test_with_right(self):
        match = Match(Either.right('python'))

        @match.when(Right)
        def case_right(v):
            return v + ' is right!'

        @match.when(Left)
        def case_left(v):
            self.fail('case_left should not called')

        self.assertEqual(match.end, 'python is right!')


    def test_with_left(self):
        match = Match(Either.left('not python'))

        @match.when(Right)
        def case_right(v):
            self.fail('case_right should not called')

        @match.when(Left)
        def case_left(v):
            return 'left because ' + v

        self.assertEqual(match.end, 'left because not python')


from masala.datatype import Stream
from masala.datatype.stream import linq_ext
from masala.datatype.stream import delete_dispatchedmethods
from masala import lambd as _l_
from masala import BuilderAllowsMethodChaining as __


class TestStreamWithLinq(unittest.TestCase):
    def setUp(self):
        reload(linq_ext)

    def test_iteration_endpoint(self):
        self.assertListEqual(
            Stream(range(0, 100)).select(__ * 2).to_list(),
            list(map(lambda x: x * 2, range(0, 100))),
        )
        self.assertListEqual(
            Stream(range(0, 100)).select(__ * 2).where(__ % 3 == 0).to_list(),
            list(filter(lambda y: y % 3 == 0, map(lambda x: x * 2, range(0, 100)))),
        )

    def test_duplicate_endpoint(self):
        with self.assertRaises(AttributeError):
            Stream(range(0, 100)).select(__ * 2).any(__ > 1000).to_list(),

    def test_method_deleted(self):
        Stream(range(0, 100)).select(_l_ * 2).any(_l_ > 1000)
        with self.assertRaises(AttributeError):
            delete_dispatchedmethods(self.linq_module_names)
            Stream(range(0, 100)).select(_l_ * 2).any(_l_ > 1000)
        reload(linq_ext)


class TestStreamWithIterTools(unittest.TestCase):

    def setUp(self):
        from masala.datatype.stream import itertools_ext

    def test_map(self):
        self.assertListEqual(
            Stream(range(5)).map_(__ * 2).to_list(),
            [0, 2, 4, 6, 8]
        )

    def test_filter(self):
        self.assertListEqual(
            Stream(range(10)).filter(__ % 2 == 0).to_list(),
            [0, 2, 4, 6, 8]
        )

    def test_endpoint(self):
        self.assertTrue(
            Stream(range(0, 100)).map_(__ * 2).any(__ < 0) is False
        )


# def load_tests(loader, tests, ignore):
#     suite = unittest.TestSuite()
#     # # FIXME: まともに動かねえクソ
#     # suite.addTests(doctest.DocFileSuite(path.join(CURRENT_DIR, 'README.md'), module_relative=False, ))
#     suite.addTests(loader.loadTestsFromTestCase(TestMatch))
#     suite.addTests(loader.loadTestsFromTestCase(TestStreamWithLinq))
#     suite.addTests(loader.loadTestsFromTestCase(TestStreamWithIterTools))
#     return tests


if __name__ == '__main__':
    doctest.ELLIPSIS = True
    doctest.NORMALIZE_WHITESPACE = True
    doctest.testfile('README.rst', optionflags=doctest.ELLIPSIS)
    unittest.main(verbosity=2)
