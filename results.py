from itertools import *
import cPickle as pickle
import datetime
from pprint import pprint

fname = 'log.pkl'
date_ix = 4

filter_by = lambda x: 'mult11' in x[0]

log = pickle.load(open(fname, 'rb'))

for day, g in groupby(ifilter(filter_by, log), key=lambda l: l[date_ix].date()):
    day_result = list(g)
    print day
    print ' avg time:', sum(r[2] for r in day_result) / float(len(day_result))
