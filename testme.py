import sys
import random
import types
import time
import itertools
import os.path
import cPickle as pickle
from datetime import datetime
from pprint import pprint




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

    @staticmethod
    def _commafy(num):
        r = []
        for i, c in enumerate(reversed(str(num))):
            if i and (not (i % 3)):
                r.insert(0, ',')
            r.insert(0, c)
        return ''.join(r)



class m11l(mathtest):
    name = "multiply by 11 (low)"

    def setup(self):
        f = random.randint(1, 9)
        f2 = random.randint(0, 9 - f)
        self.x = int(str(f) + str(f2))
        self.y = 11

    def getcorrect(self):
        return self.x * self.y

    def getprompt(self):
        return "%s * %s" % (self.x, self.y)



class m11h(mathtest):
    name = "multiply by 11 (high)"

    def setup(self):
        f = random.randint(1, 9)
        f2 = random.randint(9 - f, 9)
        self.x = int(str(f) + str(f2))
        self.y = 11

    def getcorrect(self):
        return self.x * self.y

    def getprompt(self):
        return "%s * %s" % (self.x, self.y)



class m11b(mathtest):
    name = "multiply by 11 (both)"

    def setup(self):
        self.x = random.randint(10, 99)
        self.y = 11

    def getcorrect(self):
        return self.x * self.y

    def getprompt(self):
        return "%s * %s" % (self.x, self.y)


class add3(mathtest):
    name = "add 3 digit numbers"
    hint = "add left-to-right"

    def setup(self):
        self.x = random.randint(100, 999)
        self.y = random.randint(100, 999)

    def getcorrect(self):
        return self.x + self.y

    def getprompt(self):
        return "%s + %s" % (self.x, self.y)

class add3hi(mathtest):
    name = "add 3 digit numbers, one is high"

    def setup(self):
        x = str(random.randint(100, 999))
        self.x = int(x[0] + '9' + x[2])
        self.y = random.randint(100, 999)
        if random.randint(1,2) == 1:
            swap = self.x
            self.x = self.y
            self.y = swap

    def getcorrect(self):
        return self.x + self.y

    def getprompt(self):
        return "%s + %s" % (self.x, self.y)


class add43(mathtest):
    name = "add a 4 digit and a 3 digit number"

    def setup(self):
        self.x = random.randint(1000, 9999)
        self.y = random.randint(100, 999)
        if random.randint(1,2) == 1:
            swap = self.x
            self.x = self.y
            self.y = swap

    def getcorrect(self):
        return self.x + self.y

    def getprompt(self):
        return "%s + %s" % (self.x, self.y)



class p10c(mathtest):
    name = "power of 10 complement"
    hint = "all numbers must sum to 9, except the last which must be 10"

    def setup(self):
        self.x = pow(10, random.randint(2, 6))
        self.y = random.randint(1, self.x - 1)

    def getcorrect(self):
        return self.x - self.y

    def getprompt(self):
        return "%s - %s" % (self._commafy(self.x), self._commafy(self.y))



somevar = None

possible_tests = dict(
    (somevar.__name__, somevar)
    for somevar in locals().itervalues()
    if isinstance(somevar, type) and mathtest in somevar.__bases__
    )


log_fname = 'log.pkl'

if os.path.exists(log_fname):
    log = pickle.load(open(log_fname, 'rb'))
else:
    log = []



class datedict(dict):
    # going overboard? yeah, probably
    def __getitem__(self, y):
        try:
            item = dict.__getitem__(self, y)
        except KeyError:
            return "(never)"
        assert isinstance(item, datetime)
        return item.strftime("%Y-%m-%d")


test_max_date = datedict()
for log_entry in log:
    test_max_date[log_entry[0]] = log_entry[4]


n = 0

try:
    while True:
        print "which test?"
        for key, test in sorted(possible_tests.iteritems(), key=lambda x: x[0]):
            print "%s) %s -- last taken: %s" % (key, test.name, test_max_date[key])

        choice = sys.stdin.readline().rstrip().lower()

        if choice not in possible_tests:
            print "choice not found"
            print

        else:
            chosen_test = possible_tests[choice]

            if hasattr(chosen_test, 'hint') and chosen_test.hint:
                print
                print "hint:", chosen_test.hint

            try:
                for i in itertools.count():
                    print
                    print "test", i + 1
                    testobj = chosen_test()
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
