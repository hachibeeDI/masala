# -*- coding: utf-8 -*-
from __future__ import (print_function, division, absolute_import, unicode_literals, )


if __name__ == '__main__':
    import doctest
    doctest.ELLIPSIS = True
    doctest.NORMALIZE_WHITESPACE = True
    doctest.testfile('README.rst', optionflags=doctest.ELLIPSIS)

    from os import path
    from unittest import TestLoader, TextTestRunner
    BASE_DIR = path.join(path.dirname(__file__), 'testsuites')
    testsuites = TestLoader().discover(BASE_DIR)
    TextTestRunner(verbosity=2).run(testsuites)
