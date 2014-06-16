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
        self.assertEqual(map(lambd + 2, range(3)), [2, 3, 4])


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

    def test_placeholder_with_list(self):
        match = Match({'a': 1, 'b': 2})
        @match.when([2, 2, 2], let_=('one', 'two', 'thr'))
        def case1(one, two, thr):
            return one
        @match.when({'a': 1, 'b': _}, let_=('a'))
        def case2(a):
            return a
        self.assertEqual(match.end, ('a', 1))

    def test_placeholder_with_methodcalling(self):
        match = Match('python')
        @match.when(_.startwith('aa'), let_='moo')
        def case1(moo):
            return one
        @match.when(_.startswith('pyt'), let_=('a'))
        def case2(a):
            return a
        self.assertEqual(match.end, 'python')

    def test_placeholder_with_operator(self):
        match = Match('python')
        @match.when(_.isdigit(), let_='moo')
        def case1(moo):
            return one
        @match.when(_ == 'python', let_=('a'))
        def case2(a):
            return a
        self.assertEqual(match.end, 'python')



def load_tests(loader, tests, ignore):
    suite = unittest.TestSuite()
    # FIXME: まともに動かねえクソ
    # suite.addTests(doctest.DocFileSuite(path.join(CURRENT_DIR, 'README.md'), module_relative=False, ))
    suite.addTests(loader.loadTestsFromTestCase(TestMatch))
    return tests


if __name__ == '__main__':
    doctest.testfile('README.md')
    unittest.main()
