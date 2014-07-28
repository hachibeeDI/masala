import unittest

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
