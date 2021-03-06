#!/usr/bin/env python

import sys
import random
import types
import time
import itertools
import os.path
import cPickle as pickle
from datetime import datetime
import hashlib
import gzip
from pprint import pprint

class mathtest(object):
    def getanswer (self):
        try:
            return float(sys.stdin.readline().rstrip())
        except ValueError:
            print "try again with a number"
            return self.getanswer()

    def __init__(self):
        # enforce that this is an abstract class
        # in python 2.6, can use the abc module and @abstractmethod
        assert self.__class__ != mathtest

        assert hasattr(self, 'setup')
        self.setup()

    def runtest(self):
        correct = self.getcorrect()
        print self.getprompt()

        start = time.time()
        result = self.getanswer() == correct

        diff = time.time() - start
        diffstr = "%.04fs" % diff

        if not result:
            print "correct was", correct
            if hasattr(self, 'explicate'):
                print self.explicate()

        print result, diffstr
        
        return (result, diff)

    @staticmethod
    def _commafy(num):
        "format with commas by the thousands"
        r = []
        for i, c in enumerate(reversed(str(num))):
            if i and (not (i % 3)):
                r.insert(0, ',')
            r.insert(0, c)
        return ''.join(r)

    @classmethod
    def hashme(cls):
        "hash this class definition"
        hash = hashlib.md5()
        for member in cls.__dict__.itervalues():
            if isinstance(member, types.FunctionType):
                hash.update(member.func_code.co_code)

        return hash.hexdigest()[0:16]

    @classmethod
    def getsubclasses(cls):
        for subclass in cls.__subclasses__():
            yield subclass
            for subsubclass in subclass.getsubclasses():
                yield subsubclass

    @staticmethod
    def swap(x, y):
        if random.randint(0, 1):
             x = x ^ y
             y = x ^ y
             x = x ^ y
        return (x, y)


from tests import *

possible_tests = dict(
    (subclass.__name__, subclass)
    for subclass in mathtest.getsubclasses()
    )




class datedict(dict):
    # going overboard? yeah, probably

    def __init__(self, log):
        assert hasattr(log, '__iter__')

        for log_entry in log:
            prev_record = self.get(log_entry[0]) or (0, 0, 0, 0)
            self[log_entry[0]] = (
                log_entry[4], #date
                prev_record[1] + 1, # num tries
                prev_record[2] + log_entry[3], # total time
                prev_record[3] + int(log_entry[2]) # total correct
            )

    def __getitem__(self, y):
        try:
            item = dict.__getitem__(self, y)
        except KeyError:
            return "(never taken)"
        assert isinstance(item[0], datetime)
        return "%sx last: %s, %.3fs ave %.2f%%" % (item[1], item[0].strftime("%Y-%m-%d"), item[2] / item[1], (item[3] / float(item[1]) * 100))




if __name__ == '__main__':

    log_fname = 'log.pkl.gz'

    if os.path.exists(log_fname):
        log = pickle.load(gzip.open(log_fname, 'rb'))
    else:
        log = []


    # setup tab completion
    import readline

    def completer(text, state):
        options = [x for x in possible_tests.iterkeys() if x.startswith(text)]
        try:
            return options[state]
        except IndexError:
            return None

    readline.set_completer(completer)
    readline.parse_and_bind("bind ^I rl_complete") # needed for os x 10.5 stock python install
    readline.parse_and_bind("tab: complete")

    # see the cmd module to create your own shell with its own syntax



    assert possible_tests

    n = 0

    try:
        try:
            while True:

                test_max_date = datedict(log)

                print "which test?"
                for key, test in sorted(possible_tests.iteritems(), key=lambda x: x[0]):
                    print "%s) %s -- %s" % (key, test.name, test_max_date[key])
                print "total %s tests taken" % len(log)

                choice = raw_input('> ')

                if choice not in possible_tests:
                    print "choice not found"
                    print

                else:
                    chosen_test = possible_tests[choice]

                    print
                    print chosen_test.name

                    if hasattr(chosen_test, 'hint') and chosen_test.hint:
                        print
                        print "hint:", chosen_test.hint

                    try:
                        for i in itertools.count():
                            print
                            print "test", i + 1
                            testobj = chosen_test()
                            (result, timed) = testobj.runtest()
                            log.append((testobj.__class__.__name__, testobj.hashme(), result, timed, datetime.now()))
                            n += 1
                            time.sleep(1)

                    except KeyboardInterrupt:
                        print "exiting this test..."
                        print
                        pass

        except KeyboardInterrupt:
            pass


    finally:
        print "exiting..."
        if n:
            answer = raw_input("save session? (Y)\n")
            if answer in ('', 'Y', 'YE', 'YES'):
                print "saving..."
                pickle.dump(log, gzip.open(log_fname, 'wb'))
