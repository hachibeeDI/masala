# -*- coding: utf-8 -*-
from __future__ import (print_function, division, absolute_import, unicode_literals, )

from os import path
CURRENT_DIR = path.dirname(path.abspath(__file__))

import doctest
import unittest


from masala import lambd


class TestLambdaBuilder(unittest.TestCase):

    def test_basic(self):
        from masala.datatype import Either
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


from masala.datatype import Stream
from masala.datatype.stream import delete_dispatchedmethods
from masala import lambd as _l_
from masala import BuilderAllowsMethodChaining as __


class TestStreamWithLinq(unittest.TestCase):
    def setUp(self):
        from masala.datatype.stream import linq_ext
        self.linq_module_names = linq_ext.__all__

    def test_duplicate_endpoint(self):
        with self.assertRaises(AttributeError):
            Stream(range(0, 100)).select(_l_ * 2).any(_l_ > 1000).select(_l_ + 2).to_list()

    def test_method_deleted(self):
        with self.assertRaises(AttributeError):
            delete_dispatchedmethods(self.linq_module_names)
            Stream(range(0, 100)).select(_l_ * 2).any(_l_ > 1000).select(_l_ + 2).to_list()


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

    def test_duplicate_endpoint(self):
        self.assertTrue(
            Stream(range(0, 100)).map_(_l_ * 2).any(_l_ < 0) is False
        )


def load_tests(loader, tests, ignore):
    suite = unittest.TestSuite()
    # FIXME: まともに動かねえクソ
    # suite.addTests(doctest.DocFileSuite(path.join(CURRENT_DIR, 'README.md'), module_relative=False, ))
    suite.addTests(loader.loadTestsFromTestCase(TestMatch))
    suite.addTests(loader.loadTestsFromTestCase(TestStreamWithLinq))
    suite.addTests(loader.loadTestsFromTestCase(TestStreamWithIterTools))
    return tests


if __name__ == '__main__':
    doctest.ELLIPSIS = True
    doctest.NORMALIZE_WHITESPACE = True
    doctest.testfile('README.md', optionflags=doctest.ELLIPSIS)
    unittest.main(verbosity=2)
