splendid
========

splendid is a collection of useful small python tools to make your life easier.

Visit us on https://github.com/pythoncircus/splendid !


Some Examples
-------------

    >>> from splendid import chunker
    >>> list(chunker([1, 2, 3, 4, 5], 3))
    [[1, 2, 3], [4, 5]]

    >>> from splendid import get_path
    >>> get_path({'foo':[{'bar':3}]}, ['foo'], 'not found')
    [{'bar': 3}]
    >>> get_path({'foo':[{'bar':3}]}, ['foo', 'bar'], 'not found')
    'not found'
    >>> get_path({'foo':[{'bar':3}]}, ['foo', 0, 'bar'], 'not found')
    3
    >>> get_path({'foo':[{'bar':3}]}, ['foo', 0], 'not found')
    {'bar': 3}

    >>> from splendid import run_once
    >>> @run_once
    ... def foo():
    ...     print('bar')
    >>> for i in range(10):
    ...     foo()
    bar

