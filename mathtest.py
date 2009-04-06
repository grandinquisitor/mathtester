import sys
import random
import types
import time
import itertools
import os.path
import cPickle as pickle
from datetime import datetime
import hashlib
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


class sub2b(mathtest):
    name = "2 digit subtraction, any method"

    def setup(self):
        self.x = random.randint(50, 99)
        self.y = random.randint(10, self.x-1)

    def getcorrect(self):
        return self.x - self.y

    def getprompt(self):
        return "%s - %s" % (self.x, self.y)

class sub2e(sub2b):
    name = "2 digit subtraction with no borrowing"
    hint = "86 - 25 = 86 - 20 - 5"

    def setup(self):
        self.x = random.randint(50, 99)
        x = str(self.x)
        self.y = (random.randint(1, int(x[0])) * 10) + random.randint(1, int(x[1]))
        # or: (random.randint(1, self.x // 10) * 10) + random.randint(1, self.x - ((self.x // 10) * 10)

class sub2a(sub2b):
    name = "2 digit subtraction using add-back method"
    hint = "86-28 = (86 - 30) + 2"

    def setup(self):
        self.x = (random.randint(5, 9) * 10) + random.randint(1, 8)
        x = str(self.x)
        # last digit of first number must be less than 10 minus last digit of the second number
        # in other words, 2nd digit of first number must be < 2nd digit of first number
        self.y = (random.randint(1, int(x[0])-1) * 10) + random.randint(int(x[1])+1, 9)


class sub3(sub2b):
    name = "3 digit subtraction"
    hint = "subtract the base 100, then add back the 100x complement. 534 - 467 = 534 - 500 + 33"
    # note: I find that if the complement is high or the the last two digits are less than the last two digits of the other number, it's easy to just do it the normal l2r way

    def setup(self):
        (self.y, self.x) = sorted((random.randint(100,999), random.randint(100, 999)))

class sub43(sub3):
    name = "4 digit subtraction"
    
    def setup(self):
        self.x = random.randint(1000, 9999)
        self.y = random.randint(100, 999)



somevar = None


possible_tests = dict(
    (subclass.__name__, subclass)
    for subclass in mathtest.getsubclasses()
    )


log_fname = 'log.pkl'

if os.path.exists(log_fname):
    log = pickle.load(open(log_fname, 'rb'))
else:
    log = []



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




n = 0

try:
    while True:

        test_max_date = datedict(log)

        print "which test?"
        for key, test in sorted(possible_tests.iteritems(), key=lambda x: x[0]):
            print "%s) %s -- %s" % (key, test.name, test_max_date[key])
        print "total %s tests taken" % len(log)

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
                    log.append((testobj.__class__.__name__, testobj.hashme(), result, timed, datetime.now()))
                    n += 1
                    time.sleep(1)

            except KeyboardInterrupt:
                print "exiting this test..."
                print
                pass

except KeyboardInterrupt:
    print "exiting..."

    if n:
        print "save session? (Y)"
        answer = sys.stdin.readline().rstrip().upper()
        if answer in ('', 'Y', 'YE', 'YES'):
            print "saving..."
            pickle.dump(log, open(log_fname, 'wb'))
