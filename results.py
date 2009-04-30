from itertools import *
import cPickle as pickle
import datetime
from pprint import pprint

fname = 'log.pkl'
date_ix = 4

filter_by = lambda x: 'm11h' in x[0]

log = pickle.load(open(fname, 'rb'))

for day, g in groupby(ifilter(filter_by, log), key=lambda l: l[date_ix].date()):
    day_result = list(g)
    print
    print day
    print '         n:', len(day_result)
    print ' avg score:', sum(r[2] for r in day_result) / float(len(day_result))
    print '  avg time:', sum(r[3] for r in day_result) / float(len(day_result))

print
