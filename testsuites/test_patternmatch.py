import unittest

from masala import Match
from masala import Wildcard as _
from masala.datatype import Either


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
