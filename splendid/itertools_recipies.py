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

# noinspection PyUnresolvedReferences
from six.moves import (
    filterfalse,
    map,
    range,
    zip_longest,
    zip,
)


def take(n, iterable, _list=list, _islice=islice):
    """Return first n items of the iterable as a list"""
    return _list(_islice(iterable, n))


def tabulate(function, start=0, _imap=map, _count=count):
    """Return function(0), function(1), ..."""
    return _imap(function, _count(start))


def consume(iterator, n, _deque=collections.deque, _next=next, _islice=islice):
    """Advance the iterator n-steps ahead. If n is none, consume entirely."""
    # Use functions that consume iterators at C speed.
    if n is None:
        # feed the entire iterator into a zero-length deque
        _deque(iterator, maxlen=0)
    else:
        # advance to the empty slice starting at position n
        _next(_islice(iterator, n, n), None)


def nth(iterable, n, default=None, _next=next, _islice=islice):
    """Returns the nth item or a default value"""
    return _next(_islice(iterable, n, None), default)


def all_equal(iterable, _groupby=groupby, _next=next):
    """Returns True if all the elements are equal to each other"""
    g = _groupby(iterable)
    return _next(g, True) and not _next(g, False)


def quantify(iterable, pred=bool, _sum=sum, _imap=map):
    """Count how many times the predicate is true"""
    return _sum(_imap(pred, iterable))


def padnone(iterable, _chain=chain, _repeat=repeat):
    """Returns the sequence elements and then returns None indefinitely.

    Useful for emulating the behavior of the built-in map() function.
    """
    return _chain(iterable, _repeat(None))


def ncycles(iterable, n,
            _from_iterable=chain.from_iterable, _repeat=repeat, _tuple=tuple):
    """Returns the sequence elements n times"""
    return _from_iterable(_repeat(_tuple(iterable), n))


def dotproduct(vec1, vec2, _sum=sum, _imap=map, _mul=operator.mul):
    return _sum(_imap(_mul, vec1, vec2))


def flatten(list_of_lists, _from_iterable=chain.from_iterable):
    """Flatten one level of nesting"""
    return _from_iterable(list_of_lists)


def repeatfunc(func, times=None, *args):
    """Repeat calls to func with specified arguments.

    Example:  repeatfunc(random.random)
    """
    if times is None:
        return starmap(func, repeat(args))
    return starmap(func, repeat(args, times))


def pairwise(iterable, _tee=tee, _next=next, _izip=zip):
    """s -> (s0,s1), (s1,s2), (s2, s3), ..."""
    a, b = _tee(iterable)
    _next(b, None)
    return _izip(a, b)


def grouper(iterable, n, fillvalue=None, _iter=iter, _zip_longest=zip_longest):
    """Collect data into fixed-length chunks or blocks"""
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx
    args = [_iter(iterable)] * n
    return _zip_longest(fillvalue=fillvalue, *args)


def roundrobin(*iterables):
    """roundrobin('ABC', 'D', 'EF') --> A D E B F C"""
    # Recipe credited to George Sakkis
    pending = len(iterables)
    nexts = cycle(iter(it).next for it in iterables)
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
    """powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"""
    s = _list(iterable)
    return _from_iterable(_combinations(s, r) for r in _range(_len(s)+1))


def unique_everseen(iterable, key=None, _set=set, _ifilterfalse=filterfalse):
    """List unique elements, preserving order. Remember all elements ever seen.
    """
    # unique_everseen('AAAABBBCCDAABBB') --> A B C D
    # unique_everseen('ABBCcAD', str.lower) --> A B C D
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
    """
    # unique_justseen('AAAABBBCCDAABBB') --> A B C D A B
    # unique_justseen('ABBCcAD', str.lower) --> A B C A D
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

    """
    try:
        if first is not None:
            yield first()
        while 1:
            yield func()
    except exception:
        pass


def random_product(*args, **kwds):
    """Random selection from product(*args, **kwds)"""
    pools = tuple(map(tuple, args)) * kwds.get('repeat', 1)
    choice = random.choice
    return tuple(choice(pool) for pool in pools)


def random_permutation(iterable, r=None,
                       _tuple=tuple, _len=len, _sample=random.sample):
    """Random selection from permutations(iterable, r)"""
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
    """Random selection from combinations(iterable, r)"""
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
    """Random selection from combinations_with_replacement(iterable, r)"""
    pool = _tuple(iterable)
    n = _len(pool)
    indices = _sorted(_randrange(n) for _ in _range(r))
    return _tuple(pool[i] for i in indices)


def tee_lookahead(t, i, _islice=islice):
    """Inspect the i-th upcomping value from a tee object
       while leaving the tee object at its current position.

       Raise an IndexError if the underlying iterator doesn't
       have enough values.

    """
    for value in _islice(t.__copy__(), i, None):
        return value
    raise IndexError(i)
