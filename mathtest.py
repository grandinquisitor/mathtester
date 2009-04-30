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

    @staticmethod
    def swap(x, y):
        if random.randint(0, 1):
             x = x ^ y
             y = x ^ y
             x = x ^ y
        return (x, y)


class m1(mathtest):
    name = "1-digit multiplication"

    def setup(self):
        (self.x, self.y) = self.swap(random.randint(6,9), random.randint(3,9))

    def getcorrect(self):
        return self.x * self.y

    def getprompt(self):
        return "%s * %s" % (self.x, self.y)

class m11l(m1):
    name = "multiply by 11 (low)"

    def setup(self):
        f = random.randint(1, 9)
        f2 = random.randint(1, 10 - f)
        self.x = int(str(f) + str(f2))
        self.y = 11
        self.x, self.y = self.swap(self.x, self.y)


class m11h(m1):
    name = "multiply by 11 (high)"
    hint = "add one to first digit * 100, then add second of sum of both numbers * 10, then second digit"

    def setup(self):
        f = random.randint(1, 9)
        f2 = random.randint(10 - f, 9)
        self.x = int(str(f) + str(f2))
        self.y = 11
        self.x, self.y = self.swap(self.x, self.y)



class m11b(m1):
    name = "multiply by 11 (both)"

    def setup(self):
        self.x = random.randint(10, 99)
        self.y = 11
        self.x, self.y = self.swap(self.x, self.y)


class m21(m1):
    name = "multiple 2 digit number by a 1 digit number"

    def setup(self):
        (self.x, self.y) = self.swap(random.randint(10, 99), random.randint(2, 9))


class m215(m1):
    name = "multiple 2 digit number by a 1 digit number (5s)"

    def setup(self):
        if random.randint(0, 1):
            (self.x, self.y) = self.swap(
                50 + random.randint(0, 9),
                random.randint(1, 4) * 2
            )
        else:
            (self.x, self.y) = self.swap(
                (random.randint(1, 4) * 20) + random.randint(0, 9),
                5
            )


class m21e(m1):
    name = "multiple 2 digit number by a 1 digit number, no carrying"

    def setup(self):
        self.y = random.randint(2, 9)
        x1 = random.randint(1,9)
        x2 = random.randint(0, 9 // self.y)
        self.x = (x1 * 10) + x2
        self.x, self.y = self.swap(self.x, self.y)


class m219(m1):
    name = "multiple 2 digit number by 9"

    def setup(self):
        self.x, self.y = self.swap(9, random.randint(11, 99))


class m219nc(m1):
    name = "multiple 2 digit number by 9, no carrying"

    def setup(self):
        x2 = random.randint(2, 9)
        x1 = random.randint(1, x2 - 1)
        self.x, self.y = self.swap(9, (x1 * 10) + x2)

class m2199(m1):
    name = "multiple 2 digit number by 99"
    hint = "4699 = 46x(100-1) = 4600-46 = 4554\n or : first digit, 1 minus second digit then power-of-ten complement"

    def setup(self):
        self.x, self.y = self.swap(99, random.randint(11, 99))


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
        (self.x, self.y) = self.swap(self.x, self.y)

    def getcorrect(self):
        return self.x + self.y

    def getprompt(self):
        return "%s + %s" % (self.x, self.y)


class add43(mathtest):
    name = "add a 4 digit and a 3 digit number"

    def setup(self):
        self.x = random.randint(1000, 9999)
        self.y = random.randint(100, 999)
        (self.x, self.y) = self.swap(self.x, self.y)

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


class p10cn(p10c):
    name = "power of 10 complement * n"
    hint = "all numbers must sum to 9, except the last which must be 10"

    def setup(self):
        self.x = pow(10, random.randint(2, 6)) * random.randint(2, 9)
        self.y = random.randint(1, self.x - 1)


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
        x1, x2 = random.randint(5, 9), random.randint(1, 9)
        self.x = (x1 * 10) + x2
        self.y = (random.randint(1, x1) * 10) + random.randint(1, x2)
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

class domemod(mathtest):
    # http://litemind.com/how-to-become-a-human-calendar/
    name = "domesday modulo"

    def setup(self):
        self.x = random.randint(0, 6) + random.randint(0, 6) + random.randint(1, 31)
        self.y = 7

    def getcorrect(self):
        return self.x % self.y

    def getprompt(self):
        return "%s %% %s" % (self.x, self.y)


class domecoded(mathtest):
    # http://litemind.com/how-to-become-a-human-calendar/
    name = "domesday calculations"

    def setup(self):
        self.yearcode = random.randint(0, 6)
        self.monthcode = random.randint(0, 6)
        self.day = random.randint(1, 31)

    def getcorrect(self):
        return sum((self.yearcode, self.monthcode, self.day)) % 7

    def getprompt(self):
        return "(%s + %s + %s) mod 7" % (self.yearcode, self.monthcode, self.day)



somevar = None


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

    log_fname = 'log.pkl'

    if os.path.exists(log_fname):
        log = pickle.load(open(log_fname, 'rb'))
    else:
        log = []


    n = 0

    try:
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
            pass


    finally:
        print "exiting..."
        if n:
            print "save session? (Y)"
            answer = sys.stdin.readline().rstrip().upper()
            if answer in ('', 'Y', 'YE', 'YES'):
                print "saving..."
                pickle.dump(log, open(log_fname, 'wb'))
