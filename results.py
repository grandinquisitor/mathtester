from itertools import *
import cPickle as pickle
import datetime
from pprint import pprint
import mathtest

fname = 'log.pkl'
date_ix = 4
test_name_ix = 0

keyfunc = lambda l: (l[test_name_ix], l[date_ix].date())

log = pickle.load(open(fname, 'rb'))

last_test = None

for (test, day), g in groupby(sorted(log, key=keyfunc), key=keyfunc):

    if test != last_test:
        print
        print
        try:
            name = "%s (%s)" % (test, mathtest.possible_tests[test].name)
        except:
            name = test
        print name + "::"
        last_test = test

    day_result = list(g)
    print
    print ' ' + str(day)
    print '          n:', len(day_result)
    print '  avg score:', sum(r[2] for r in day_result) / float(len(day_result))
    print '   avg time:', sum(r[3] for r in day_result) / float(len(day_result))

print
