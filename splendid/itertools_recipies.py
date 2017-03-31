# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
'''Convenience version of the itertool recipies found in python docs.

These were initially copied from
https://docs.python.org/2/library/itertools.html#recipes .

Main changes:
- code formatting
- doctests
- python 2 and 3 compatibility via six
- optimization by replacing global lookups with local default vars
'''

import collections
from itertools import chain
from itertools import combinations
from itertools import count
from itertools import cycle
from itertools import groupby
from itertools import islice
from itertools import repeat
from itertools import starmap
from itertools import tee

import operator
from operator import itemgetter
import random

from six import PY2
# noinspection PyUnresolvedReferences
from six.moves import (
    filterfalse,
    map,
    range,
    zip_longest,
    zip,
)


def take(n, iterable, _list=list, _islice=islice):
    """Return first n items of the iterable as a list.

    >>> c = count()
    >>> take(5, c)
    [0, 1, 2, 3, 4]
    >>> take(5, c)
    [5, 6, 7, 8, 9]

    Missing values won't be filled:
    >>> take(5, [1, 2, 3])
    [1, 2, 3]
    >>> take(0, [1, 2, 3])
    []
    """
    return _list(_islice(iterable, n))


def tabulate(f, start=0, _imap=map, _count=count):
    """Return function(0), function(1), ...

    >>> def square(x):
    ...     return x*x
    >>> take(5, tabulate(square))
    [0, 1, 4, 9, 16]
    """
    return _imap(f, _count(start))


def consume(iterator, n, _deque=collections.deque, _next=next, _islice=islice):
    """Advance the iterator n-steps ahead. If n is none, consume entirely.

    >>> l = [1, 2, 3, 4, 5, 6]
    >>> it = iter(l)
    >>> next(it)
    1
    >>> consume(it, 2)
    >>> next(it)
    4
    >>> consume(it, None)
    >>> list(it)
    []
    
    >>> it = count()
    >>> consume(it, 3)
    >>> next(it)
    3
    """
    # Use functions that consume iterators at C speed.
    if n is None:
        # feed the entire iterator into a zero-length deque
        _deque(iterator, maxlen=0)
    else:
        # advance to the empty slice starting at position n
        _next(_islice(iterator, n, n), None)


def nth(iterable, n, default=None, _next=next, _islice=islice):
    """Returns the nth item or a default value.

    >>> l = [1, 1, 2, 3, 5, 8, 13]
    >>> nth(l, 0)
    1
    >>> nth(l, 1)
    1
    >>> nth(l, 5)
    8
    >>> nth(l, 10) is None
    True
    """
    return _next(_islice(iterable, n, None), default)


def all_equal(iterable, _groupby=groupby, _next=next):
    """Returns True if all the elements are equal to each other.

    >>> all_equal([2, 2, 2, 2])
    True
    >>> all_equal(count())
    False
    >>> all_equal([])
    True
    >>> all_equal([True, True])
    True
    >>> all_equal([False, False])
    True
    >>> all_equal([True, False])
    False
    >>> all_equal([False, True])
    False
    """
    g = _groupby(iterable)
    return _next(g, True) and not _next(g, False)


def quantify(iterable, pred=bool, _sum=sum, _imap=map):
    """Count how many times the predicate is true.

    >>> quantify([True, False, True, True, False])
    3
    >>> quantify(range(20))
    19
    >>> quantify(range(20), lambda x: x < 10)
    10
    """
    return _sum(_imap(pred, iterable))


def padnone(iterable, _chain=chain, _repeat=repeat):
    """Returns the sequence elements and then returns None indefinitely.

    Useful for emulating the behavior of the built-in map() function.

    >>> pn = padnone([1, 2, 3])
    >>> take(5, pn)
    [1, 2, 3, None, None]
    """
    return _chain(iterable, _repeat(None))


def ncycles(iterable, n,
            _from_iterable=chain.from_iterable, _repeat=repeat, _tuple=tuple):
    """Returns the sequence elements n times.

    Notice that while n can be very large, the iterable is initially turned into
    a tuple! Hence, this does NOT work on infinite iterables!

    >>> list(ncycles("abcd", 3))
    ['a', 'b', 'c', 'd', 'a', 'b', 'c', 'd', 'a', 'b', 'c', 'd']
    >>> take(7, ncycles(range(5), 10000))
    [0, 1, 2, 3, 4, 0, 1]
    """
    return _from_iterable(_repeat(_tuple(iterable), n))


def dotproduct(vec1, vec2, _sum=sum, _imap=map, _mul=operator.mul):
    """Calculates the dot-product of two vectors.

    If you do a lot of computations with vectors, we recommend to have a look at
    numpy and its numpy.dot() function. For a single calculation however this
    method is competitive. Also this method will work in case vec1 and vec2 are
    too large to fit into memory.

    >>> dotproduct([1, 2, 3], [4, 5, 6])
    32
    >>> dotproduct(range(10000), repeat(0))
    0
    """
    return _sum(_imap(_mul, vec1, vec2))


def flatten(list_of_lists, _from_iterable=chain.from_iterable):
    """Flatten one level of nesting.

    >>> list(flatten([[1, 2, 3], [4, 5, 6]]))
    [1, 2, 3, 4, 5, 6]
    >>> list(flatten([[[1]], [2, 3], [4, [5, [6]]]]))
    [[1], 2, 3, 4, [5, [6]]]

    Also works on infinite lists of lists:

    >>> take(3, repeat([1, 2]))
    [[1, 2], [1, 2], [1, 2]]
    >>> take(3, flatten(repeat([1, 2])))
    [1, 2, 1]
    """
    return _from_iterable(list_of_lists)


def repeatfunc(func, times=None, *args):
    """Repeat calls to func with specified arguments.

    >>> list(repeatfunc(take, 5, 2, [1, 2, 3]))
    [[1, 2], [1, 2], [1, 2], [1, 2], [1, 2]]
    """
    if times is None:
        return starmap(func, repeat(args))
    return starmap(func, repeat(args, times))


def pairwise(iterable, _tee=tee, _next=next, _izip=zip):
    """s -> (s0,s1), (s1,s2), (s2, s3), ...

    Generates a pairwise window that overlaps.

    >>> list(pairwise('hello'))
    [('h', 'e'), ('e', 'l'), ('l', 'l'), ('l', 'o')]
    >>> list(pairwise([1, 2, 3, 4]))
    [(1, 2), (2, 3), (3, 4)]
    >>> list(pairwise([1]))
    []
    >>> take(5, pairwise(count()))
    [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5)]
    """
    a, b = _tee(iterable)
    _next(b, None)
    return _izip(a, b)


def grouper(iterable, n, fillvalue=None, _iter=iter, _zip_longest=zip_longest):
    """Collect data into fixed-length chunks or blocks.

    >>> list(grouper('ABCDEFG', 3, 'x'))
    [('A', 'B', 'C'), ('D', 'E', 'F'), ('G', 'x', 'x')]
    >>> list(grouper('ABCDEFG', 3))
    [('A', 'B', 'C'), ('D', 'E', 'F'), ('G', None, None)]
    >>> take(2, grouper(count(), 3))
    [(0, 1, 2), (3, 4, 5)]
    """
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx
    args = [_iter(iterable)] * n
    return _zip_longest(fillvalue=fillvalue, *args)


def roundrobin(*iterables):
    """roundrobin('ABC', 'D', 'EF') --> A D E B F C
    
    >>> list(roundrobin('ABC', 'D', 'EF'))
    ['A', 'D', 'E', 'B', 'F', 'C']
    >>> take(7, roundrobin(count(), count(10), 'A'))
    [0, 10, 'A', 1, 11, 2, 12]
    """
    # Recipe credited to George Sakkis
    pending = len(iterables)
    if PY2:
        nexts = cycle(iter(it).next for it in iterables)
    else:
        nexts = cycle(iter(it).__next__ for it in iterables)
    while pending:
        try:
            for next_ in nexts:
                yield next_()
        except StopIteration:
            pending -= 1
            nexts = cycle(islice(nexts, pending))


def powerset(
        iterable,
        _list=list,
        _from_iterable=chain.from_iterable,
        _combinations=combinations,
        _range=range,
        _len=len
):
    """powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)
    
    >>> list(powerset([1, 2, 3]))
    [(), (1,), (2,), (3,), (1, 2), (1, 3), (2, 3), (1, 2, 3)]
    """
    s = _list(iterable)
    return _from_iterable(_combinations(s, r) for r in _range(_len(s)+1))


def unique_everseen(iterable, key=None, _set=set, _ifilterfalse=filterfalse):
    """List unique elements, preserving order. Remember all elements ever seen.
    
    >>> list(unique_everseen('AAAABBBCCDAABBB'))
    ['A', 'B', 'C', 'D']
    >>> list(unique_everseen('ABDCABCD'))
    ['A', 'B', 'D', 'C']
    >>> list(unique_everseen('ABBCcAD', str.lower))
    ['A', 'B', 'C', 'D']
    
    Works on infinite lists (uses memory for each new element):
    >>> take(5, unique_everseen(roundrobin(count(), count(10), count())))
    [0, 10, 1, 11, 2]
    """
    seen = _set()
    seen_add = seen.add
    if key is None:
        for element in _ifilterfalse(seen.__contains__, iterable):
            seen_add(element)
            yield element
    else:
        for element in iterable:
            k = key(element)
            if k not in seen:
                seen_add(k)
                yield element


def unique_justseen(iterable, key=None,
                    _imap=map, _itemgetter=itemgetter(1), _groupby=groupby):
    """List unique elements, preserving order. Remember only element just seen.
    
    >>> list(unique_justseen('AAAABBBCCDAABBB'))
    ['A', 'B', 'C', 'D', 'A', 'B']
    >>> list(unique_justseen('ABBCcAD', str.lower))
    ['A', 'B', 'C', 'A', 'D']
    
    Works on infinite lists (only remembers last element):
    >>> take(7, unique_justseen(roundrobin(count(), count(10), count())))
    [0, 10, 0, 1, 11, 1, 2]
    """
    return _imap(next, _imap(_itemgetter, _groupby(iterable, key)))


def iter_except(func, exception, first=None):
    """ Call a function repeatedly until an exception is raised.

    Converts a call-until-exception interface to an iterator interface.
    Like __builtin__.iter(func, sentinel) but uses an exception instead
    of a sentinel to end the loop.

    Examples:
        bsddbiter = iter_except(db.next, bsddb.error, db.first)
        heapiter = iter_except(functools.partial(heappop, h), IndexError)
        dictiter = iter_except(d.popitem, KeyError)
        dequeiter = iter_except(d.popleft, IndexError)
        queueiter = iter_except(q.get_nowait, Queue.Empty)
        setiter = iter_except(s.pop, KeyError)
    
    >>> s = {1, 2, 3}
    >>> setiter = iter_except(s.pop, KeyError)
    >>> sorted(setiter)
    [1, 2, 3]
    >>> len(s)
    0
    
    >>> d = {1: 2}
    >>> dictiter = iter_except(d.popitem, KeyError, lambda: 'init')
    >>> list(dictiter)
    ['init', (1, 2)]
    """
    try:
        if first is not None:
            yield first()
        while 1:
            yield func()
    except exception:
        pass


def random_product(*args, **kwds):
    """Random selection from product(*args, **kwds)
    
    >>> random.seed(1)
    >>> random_product([1, 2, 3], [4, 5, 6])
    (1, 6)
    """
    pools = tuple(map(tuple, args)) * kwds.get('repeat', 1)
    choice = random.choice
    return tuple(choice(pool) for pool in pools)


def random_permutation(iterable, r=2,
                       _tuple=tuple, _len=len, _sample=random.sample):
    """Random selection from permutations(iterable, r)
    
    >>> random.seed(11)
    >>> random_permutation([1, 2, 3])
    (2, 3)
    """
    pool = _tuple(iterable)
    r = _len(pool) if r is None else r
    return _tuple(_sample(pool, r))


def random_combination(
        iterable, r,
        _tuple=tuple,
        _len=len,
        _sorted=sorted,
        _sample=random.sample,
        _range=range
):
    """Random selection from combinations(iterable, r)
    
    >>> random.seed(0)
    >>> random_combination([1, 2, 3], 2)
    (2, 3)
    """
    pool = _tuple(iterable)
    n = _len(pool)
    indices = _sorted(_sample(_range(n), r))
    return _tuple(pool[i] for i in indices)


def random_combination_with_replacement(
        iterable, r,
        _tuple=tuple,
        _len=len,
        _sorted=sorted,
        _randrange=random.randrange,
        _range=range
):
    """Random selection from combinations_with_replacement(iterable, r)
    
    >>> random.seed(42)
    >>> random_combination_with_replacement([1, 2, 3], 6)
    (1, 1, 1, 2, 3, 3)
    """
    pool = _tuple(iterable)
    n = _len(pool)
    indices = _sorted(_randrange(n) for _ in _range(r))
    return _tuple(pool[i] for i in indices)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
