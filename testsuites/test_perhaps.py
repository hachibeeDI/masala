# -*- coding: utf-8 -*-
from __future__ import (print_function, division, absolute_import, unicode_literals, )

import unittest

from masala import Perhaps


class TestPerhaps(unittest.TestCase):

    def test_basic(self):
        st = Perhaps("hoge")._.upper()._.replace('H', 'n')
        self.assertEqual(st._, 'nOGE')

    def test_nullsafe(self):
        null = Perhaps(None)._.upper()._.replace('H', 'n')
        self.assertIs(null.get(), None)
        self.assertEqual(null.get_or('py'), 'py')

    def test_shift(self):
        apply_case = (
            Perhaps(range(10)) >>
            (lambda xs: [x * 2 for x in xs]) >>
            (lambda xs: [x for x in xs if x % 4 == 0]))
        self.assertEqual(apply_case._, [0,  4,  8,  12,  16])

    def test_direct(self):
        st = Perhaps("hoge").upper().replace('H', 'n')
        self.assertEqual(st._, 'nOGE')


    def test_nulldirect(self):
        with self.assertRaises(AttributeError):
            Perhaps(None).upper().replace('H', 'n')
