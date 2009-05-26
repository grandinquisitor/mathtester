#!/usr/bin/env python

from itertools import *
import cPickle as pickle
import datetime
from pprint import pprint
import mathtest
import numpy

fname = 'log.pkl'
date_ix = 4
test_name_ix = 0

keyfunc = lambda l: l[test_name_ix]
keyfunc2 = lambda x: x[4].timetuple()[:5]

log = pickle.load(open(fname, 'rb'))

last_test = None

print
print '      test    n  av score  sc trend  sc y-int  av time time trend time y-int'


sums = [0] + ([0.0] * 6)

for test, g in groupby(sorted(log, key=keyfunc), key=keyfunc):
    if test not in mathtest.possible_tests:
        continue

    g = list(g)
    n = len(g)
    x = range(n)

    y = [float(y[2]) for y in g]
    m, b = numpy.polyfit(x, y, 1)
    a = sum(y) / n

    y2 = [y2[3] for y2 in g]
    m2, b2 = numpy.polyfit(x, y2, 1)
    a2 = sum(y2) / n

    sums[0] += 1

    sums[1] += a
    sums[2] += m
    sums[3] += b
    sums[4] += a2
    sums[5] += m2
    sums[6] += b2

    print "%10s %4i  %4f % 5f  %5f  %07.4f % 5f  %#08.5f" % (test, n, a, m, b, a2, m2, b2)

    
print "%10s %4i  %4f % 5f  %5f  %07.4f % 5f  %#08.5f" % ('(avg)', sums[0], sums[1]/sums[0], sums[2]/sums[0], sums[3]/sums[0], sums[4]/sums[0], sums[5]/sums[0], sums[6]/sums[0])


print
