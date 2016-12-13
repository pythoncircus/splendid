# -*- coding: utf-8 -*-
"""Splendid, a collection of useful, small python tools."""
from __future__ import print_function

from codecs import open
from os import path
from setuptools import setup

from splendid.version import __version__


ROOT = path.abspath(path.dirname(__file__))


# Use the README as the long description
with open(path.join(ROOT, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='splendid',
    version=__version__,
    description=__doc__,
    long_description=long_description,
    url='https://github.com/pythoncircus/splendid',
    author='Joachim Folz, Jörn Hees',
    author_email='joachim.folz+splendid@gmail.com, splendid@joernhees.de',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development',
        'Topic :: Utilities',
    ],
    keywords='splendid tools utils wrappers useful small often needed',
    packages=['splendid'],
)
