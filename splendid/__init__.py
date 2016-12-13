# -*- coding: utf-8 -*-

from version import __version__

from functools import wraps
from itertools import izip_longest
from timeit import default_timer as timer


__all__ = [
    'chunker',
    'get_path',
    'run_once',
    'time_func',
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
        for t in izip_longest(*args, fillvalue=fillvalue)
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
    """
    rest = nested
    for key in key_path:
        try:
            rest = rest[key]
        except (LookupError, TypeError):
            return default
    return rest


def run_once(func):
    """Decorator that causes a function to be executed only once."""
    @wraps(func)
    def wrapper(*args, **kwds):
        if not wrapper.ran:
            wrapper.ran = True
            return func(*args, **kwds)
    wrapper.ran = False
    return wrapper


def time_func(func, *args, **kwds):
    """Calls func with given args and returns a (timediff, res) tuple.

    :param func: function to be evaluated
    :param args: args for func
    :param kwds: kwds for func
    :return: a tuple: (timediff, func(*args, **kwds)
    """
    start = timer()
    res = func(*args, **kwds)
    stop = timer()
    return stop - start, res


