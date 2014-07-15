# -*- coding: utf-8 -*-


from setuptools import (
    setup,
    find_packages,
)

VERSION = '0.0.2'


with open('README.rst') as f:
    LONG_DESCRIPTION = f.read()


setup(
    name='masala',
    version=VERSION,
    packages=find_packages(),
    install_requires=['six'],
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
