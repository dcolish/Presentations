import speedyc
from timeit import timeit


def runit(var):
    ll = 0
    for x in xrange(var):
        ll += x ** 2
    return ll

t = 10 ** 4

print timeit("runit(t)", "from __main__ import runit, t",
       number=1000)

print timeit("speedyc.crunit(t)", "from __main__ import speedyc, t",
       number=1000)
