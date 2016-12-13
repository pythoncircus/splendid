# -*- coding: utf-8 -*-
import time
from splendid import time_func


def foo(*args, **kwds):
    return args, kwds


t, r = time_func(foo, 1, 2, 3, bar=4, bla='blub')
assert isinstance(t, float)
assert t < 1.
assert r == ((1, 2, 3), {'bar': 4, 'bla': 'blub'})


def foo_wait(a, b):
    time.sleep(1.25)
    return a + b


t, r = time_func(foo_wait, 1, b=2)
assert t > 1.25
assert r == 3
