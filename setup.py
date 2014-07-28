# -*- coding: utf-8 -*-
from __future__ import (print_function, division, absolute_import, )

from sys import version_info

from setuptools import (
    setup,
    find_packages,
)

VERSION = '0.0.2'


with open('README.rst') as f:
    LONG_DESCRIPTION = f.read()

REQUIRES = []
with open('requirements.txt') as f:
    REQUIRES.extend(l.strip() for l in f.readlines())


if version_info[0] == 2:
    with open('requirements_27.txt') as f:
        REQUIRES.extend(l.strip() for l in f.readlines())
REQUIRES = [r for r in REQUIRES if r]

setup(
    name='masala',
    version=VERSION,
    packages=find_packages(),
    install_requires=REQUIRES,
    author='OGURA_Daiki',
    author_email='8hachibee125@gmail.com',
    license='MIT',
    url='https://github.com/hachibeeDI/masala',
    description='curry functional patternpatch linq',
    long_description=LONG_DESCRIPTION,
    classifiers='''
Programming Language :: Python
Development Status :: 4 - Beta
License :: OSI Approved :: MIT License
Programming Language :: Python :: 2
Programming Language :: Python :: 2.7
Programming Language :: Python :: 3
Programming Language :: Python :: 3.4
Topic :: Software Development :: Libraries :: Python Modules
Topic :: Utilities
'''.strip().splitlines())
