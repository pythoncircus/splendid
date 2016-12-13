# -*- coding: utf-8 -*-
"""Splendid, a collection of useful, small python tools."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from codecs import open
from os import path
from setuptools import setup


ROOT = path.abspath(path.dirname(__file__))


# Use the README as the long description
with open(path.join(ROOT, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


# extract version from splendid/__init__.py
with open(path.join(ROOT, 'splendid', '__init__.py'), encoding='utf-8') as f:
    version = None
    for line in f:
        if line.startswith('__version__ = '):
            version = line.split('=')[1].split('#')[0]\
                .strip().strip('"').strip("'")
            break
    else:
        raise SyntaxError('could not find __version__')


requirements = [
    'six',
]

setup(
    name='splendid',
    version=version,
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
    install_requires=requirements,
    setup_requires=['pytest-runner'],
    tests_require=requirements + [
        'pytest',
    ],
    zip_safe=True,
)
