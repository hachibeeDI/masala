# -*- coding: utf-8 -*-


import setuptools

VERSION = '0.0.1'


setuptools.setup(
    name='masala',
    version=VERSION,
    packages=['masala'],
    install_requires=['six'],
    author='OGURA_Daiki',
    author_email='8hachibee125@gmail.com',
    license='MIT',
    url='https://github.com/hachibeeDI/masala',
    description='curry functional patternpatch linq',
    long_description='',
    classifiers='''
Programming Language :: Python
Development Status :: 2 - Pre-Alpha
License :: OSI Approved :: MIT License
Programming Language :: Python :: 2
Programming Language :: Python :: 2.7
Programming Language :: Python :: 3
Programming Language :: Python :: 3.4
Topic :: Software Development :: Libraries :: Python Modules
Topic :: Utilities
'''.strip().splitlines())
