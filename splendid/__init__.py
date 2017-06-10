# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
"""Splendid, a collection of useful small python tools.

https://github.com/pythoncircus/splendid
"""

import datetime
import os
import random
from functools import wraps
from timeit import default_timer as timer

# noinspection PyUnresolvedReferences
from six.moves import zip_longest


# we use http://semver.org
__version__ = '1.1.0'

__all__ = [
    'chunker',
    'get_path',
    'make_dirs_for',
    'randbool',
    'run_once',
    'time_func',
    'timedelta_to_microseconds',
    'timedelta_to_ms',
    'timedelta_to_s',
]


def chunker(iterable, n, fillvalue=None, dtype=list):
    """Like a grouper but last tuple is shorter.

    >>> list(chunker([1, 2, 3, 4, 5], 3))
    [[1, 2, 3], [4, 5]]
    """
    if n < 1:
        raise ValueError("can't chunk by n=%d" % n)
    args = [iter(iterable)] * n
    return (
        dtype(e for e in t if e is not None)
        for t in zip_longest(*args, fillvalue=fillvalue)
    )


def get_path(
        nested,
        key_path,
        default=None,
        expected_errors=(LookupError, TypeError)):
    """Walk given dicts/lists by key_path returning default on any LookupError.

    Useful to quickly extract information from nested data structures. Typical
    examples are nested dicts and lists that you for example obtained from
    `json.loads()`.

    >>> get_path({'foo':[{'bar':3}]}, ['foo'], 'not found')
    [{'bar': 3}]
    >>> get_path({'foo':[{'bar':3}]}, ['foo', 'bar'], 'not found')
    'not found'
    >>> get_path({'foo':[{'bar':3}]}, ['foo', 0, 'bar'], 'not found')
    3
    >>> get_path({'foo':[{'bar':3}]}, ['foo', 0], 'not found')
    {'bar': 3}

    :param nested: a nested dictionary or list like structure
    :param key_path: an iterable resembling a path of keys
    :param default: returned if any key in the path isn't found
    :param expected_errors: expected errors, use for custom data structures
    :return: value of nested[k0][k1]...[kn] or default (default: None) on error
    """
    rest = nested
    for key in key_path:
        try:
            rest = rest[key]
        except expected_errors:
            return default
    return rest


def make_dirs_for(file_path):
    """Try to create all necessary directories for file.

    Use like this:
    with open(make_dirs_for(my_filepath), 'w') as f:
        f.write("hello world")
    """
    try:
        os.makedirs(os.path.dirname(file_path))
    except OSError:
        pass
    return file_path


def randbool():
    """Randomly return True or False.

    >>> random.seed(43)
    >>> randbool()
    False
    >>> randbool()
    True
    """
    return bool(random.randint(0, 1))


def remove_prefix(s, prefix, length=None):
    """Remove prefix from s if exists.

    >>> remove_prefix('foobar', 'foo')
    'bar'
    >>> remove_prefix('foobar', 'bar')
    'foobar'
    >>> remove_prefix('foobar', 'foo', 1)
    'oobar'
    """
    if s.startswith(prefix):
        return s[length or len(prefix):]
    return s


def run_once(func):
    """Decorator that causes a function to be executed only once.
    >>> @run_once
    ... def foo():
    ...     print('bar')
    >>> for i in range(10):
    ...     foo()
    bar
    """
    @wraps(func)
    def wrapper(*args, **kwds):
        if not wrapper.ran:
            wrapper.ran = True
            return func(*args, **kwds)
    wrapper.ran = False
    return wrapper


def time_func(func, *args, **kwds):
    """Calls func with given args and returns a (seconds, res) tuple.

    >>> def foo(a, b):
    ...    return a + b
    >>> t, res = time_func(foo, 1, b=2)
    >>> res
    3
    >>> isinstance(t, float)
    True
    >>> t < 1.
    True

    :param func: function to be evaluated
    :param args: args for func
    :param kwds: kwds for func
    :return: a tuple: (seconds, func(*args, **kwds)
    """
    start = timer()
    res = func(*args, **kwds)
    stop = timer()
    return stop - start, res


def timedelta_to_microseconds(td):
    """Convert a timedelta object into microseconds.

    Also see timedelta_to_ms and timedelta_to_s below.

    >>> dt1 = datetime.datetime(2010, 10, 28, 19, 14, 12, 1539)
    >>> dt1
    datetime.datetime(2010, 10, 28, 19, 14, 12, 1539)
    >>> dt2 = datetime.datetime(2010, 10, 28, 19, 15, 12, 298)

    Notice how dt1 is nearly a minute before dt2:
    >>> print(dt2 - dt1)
    0:00:59.998759
    >>> print(timedelta_to_s(dt2 - dt1))
    59.998759
    >>> print(timedelta_to_ms(dt2 - dt1))
    59998.759
    >>> print(timedelta_to_microseconds(dt2 - dt1))
    59998759

    Now the following shows some weirdness in formatting -1 day + 23:59 h
    makes ~1 minute:
    >>> print(dt1 - dt2)
    -1 day, 23:59:00.001241

    If all is expressed in ms:
    >>> print(timedelta_to_s(dt1 - dt2))
    -59.998759

    >>> print(timedelta_to_microseconds(dt1 - dt1))
    0
    >>> dt3 = datetime.datetime(2010, 10, 28, 19, 15, 12, 297000)
    >>> print(timedelta_to_ms(dt2 - dt3))
    -296.702
    >>> dt4 = datetime.datetime(2010, 10, 28, 19, 15, 12, 298000)
    >>> print(timedelta_to_ms(dt4 - dt3))
    1.0

    :param td: a timedelta object
    """
    return (
        td.days * 24 * 60 * 60 * 1000000
        + td.seconds * 1000000
        + td.microseconds
    )


def timedelta_to_ms(td):
    return timedelta_to_microseconds(td) / 1000


def timedelta_to_s(td):
    return timedelta_to_microseconds(td) / 1000000



if __name__ == '__main__':
    import doctest
    doctest.testmod()
