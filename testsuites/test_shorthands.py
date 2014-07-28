import unittest

from masala import lambd
from masala.datatype import Either


class TestLambdaBuilder(unittest.TestCase):

    def test_basic(self):
        self.assertEqual(Either.right('hachi') >> lambd.title(), u'Hachi')
        self.assertEqual(list(map(lambd + 2, range(3))), [2, 3, 4])
