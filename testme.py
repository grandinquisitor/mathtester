import sys
import random
import types
import time
import itertools
import os.path
import cPickle as pickle
from datetime import datetime




class mathtest(object):
    def getanswer (self):
        try:
            return float(sys.stdin.readline().rstrip())
        except ValueError:
            print "try again with a number"
            return self.getanswer()

    def __init__(self):
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

        print result, diffstr
        
        return (result, diff)




class mult11l(mathtest):
    name = "multiply by 11 (low)"
    key = "m11l"

    def setup(self):
        f = random.randint(1, 9)
        f2 = random.randint(0, 9 - f)
        self.x = int(str(f) + str(f2))
        self.y = 11

    def getcorrect(self):
        return self.x * self.y

    def getprompt(self):
        return "%s * %s" % (self.x, self.y)



class mult11h(mathtest):
    name = "multiply by 11 (high)"
    key = "m11h"

    def setup(self):
        f = random.randint(1, 9)
        f2 = random.randint(9 - f, 9)
        self.x = int(str(f) + str(f2))
        self.y = 11

    def getcorrect(self):
        return self.x * self.y

    def getprompt(self):
        return "%s * %s" % (self.x, self.y)



class mult11b(mathtest):
    name = "multiply by 11 (both)"
    key = "m11b"

    def setup(self):
        self.x = random.randint(10, 99)
        self.y = 11

    def getcorrect(self):
        return self.x * self.y

    def getprompt(self):
        return "%s * %s" % (self.x, self.y)




somevar = None

possible_tests = dict(
    (somevar.key, somevar)
    for somevar in locals().itervalues()
    if isinstance(somevar, type) and mathtest in somevar.__bases__
    )


log_fname = 'log.pkl'

if os.path.exists(log_fname):
    log = pickle.load(open(log_fname, 'rb'))
else:
    log = []

n = 0

try:
    while True:
        print "which test?"
        for key, test in possible_tests.iteritems():
            print "%s) %s" % (key, test.name)

        choice = sys.stdin.readline().rstrip().lower()

        if choice not in possible_tests:
            print "choice not found"
            print

        else:
            try:
                for i in itertools.count():
                    print
                    print "test", i + 1
                    testobj = possible_tests[choice]()
                    (result, timed) = testobj.runtest()
                    log.append((testobj.__class__.__name__, object.__hash__(testobj.__class__), result, timed, datetime.now()))
                    n += 1
                    time.sleep(1)

            except KeyboardInterrupt:
                print "exiting this test..."
                print
                pass

except KeyboardInterrupt:
    print "exiting..."
finally:
    if n:
        print "save session? (Y)"
        answer = sys.stdin.readline().rstrip().upper()
        if answer in ('', 'Y', 'YE', 'YES'):
            print "saving..."
            pickle.dump(log, open(log_fname, 'wb'))
