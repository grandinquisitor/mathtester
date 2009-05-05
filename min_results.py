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

sums = [0] + ([0.0] * 4)
for test, g in groupby(sorted(log, key=keyfunc), key=keyfunc):
    g = list(g)
    n = len(g)
    x = range(n)

    y = [float(y[2]) for y in g]
    m, b = numpy.polyfit(x, y, 1)

    y2 = [y[3] for y in g]
    m2, b2 = numpy.polyfit(x, y2, 1)

    sums[0] += 1

    sums[1] += m
    sums[2] += b
    sums[3] += m2
    sums[4] += b2

    print "%10s %4i  % 5f  %5f  % 5f  %#08.5f" % (test, n, m, b, m2, b2)

    
print "%10s %4i  % 5f  %5f  % 5f  %#08.5f" % ('(avg)', sums[0], sums[1]/sums[0], sums[2]/sums[0], sums[3]/sums[0], sums[4]/sums[0])


print
