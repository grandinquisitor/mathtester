from mathtest import *

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
        f = random.randint(1, 8)
        f2 = random.randint(1, 9 - f)
        f, f2 = self.swap(f, f2)
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

class m215b(m1):
    name = "multiply 5 by odd numbers"
    hint = "if 2nd digit1: 55, 2: 60, 3: 65, 4: 70.... you should never need to carry"

    def setup(self):
        self.x = (((random.randint(0,4) * 2) + 1) * 10) + random.randint(1,9)
        self.y = 5
        self.x, self.y = self.swap(self.x, self.y)


class m21e(m1):
    name = "multiply 2 digit number by a 1 digit number, no carrying"

    def setup(self):
        self.y = random.randint(2, 9)
        x1 = random.randint(1,9)
        x2 = random.randint(0, 9 // self.y)
        self.x = (x1 * 10) + x2
        self.x, self.y = self.swap(self.x, self.y)


class m219(m1):
    name = "multiply 2 digit number by 9"
    hint = "x * 99 = (x * 100) - x. if it ends in 1 or 0, however, do it the usual way"

    def setup(self):
        self.x, self.y = self.swap(9, random.randint(11, 99))


class m219nc(m1):
    name = "multiply 2 digit number by 9, no borrowing"

    def setup(self):
        x2 = random.randint(2, 9)
        x1 = random.randint(1, x2 - 1)
        self.x, self.y = self.swap(9, (x1 * 10) + x2)


class m219c(m1):
    name = "multiply 2 digit number by 9, only borrowing"

    def setup(self):
        # 2nd digit must be equal or lt 1 digit
        x1 = random.randint(1, 9)
        x2 = random.randint(1, x1)
        self.x, self.y = self.swap(9, (x1 * 10) + x2)


class m2199(m1):
    name = "multiply 2 digit number by 99"
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


class sub3a(sub2b):
    name = "3 digit subtraction, add-back method"
    hint = "subtract the base 100, then add back the 100x complement. 534 - 467 = 534 - 500 + 33"
    # note: I find that if the complement is high or the the last two digits are less than the last two digits of the other number, it's easy to just do it the normal l2r way

    def setup(self):
        x1, y1 = sorted((random.randint(1, 99), random.randint(1, 99)))
        self.x = (random.randint(1, 9) * 100) + x1
        self.y = (random.randint(1, self.x // 100) * 100) + y1


class sub3e(sub2b):
    name = "3 digit subtraction, no borrowing"
    hint = "adding back the 100x complement should not be needed"

    def setup(self):
        y1, x1 = sorted((random.randint(1, 99), random.randint(1, 99)))
        self.x = (random.randint(1, 9) * 100) + x1
        self.y = (random.randint(1, self.x // 100) * 100) + y1


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


class ycode(mathtest):
    name = "year code calculations"
    hint = "2-digit year truncated division by 4, then add back the year, then mod 7, and add 1 for 19xx"

    def setup(self):
        self.year = random.randint(1900, 2099)

    @staticmethod
    def calc_year_code(y):
        assert 1900 <= y <= 2099
        yy = y % 100
        step1 = yy // 4
        step2 = step1 + yy
        step3 = step2 % 7
        step4 = int(y <= 1999)
        ans = step3 + step4
        return (yy, step1, step2, step3, step4, ans)

    def getcorrect(self):
        return self.calc_year_code(self.year)[5]

    def explicate(self):
        parts = self.calc_year_code(self.year)
        return """
%s
%s // 4 == %s
%s + %s == %s
%s %% 7 == %s
+ %s = %s
"""     %   (parts[0], 
             parts[0], parts[1], 
             parts[1], parts[0], parts[2], 
             parts[2], parts[3],
             parts[4], parts[5])

    def getprompt(self):
        return "%s" % self.year


class mod4(mathtest):
    name = "modulo 4"
    mod = 4

    def setup(self):
        self.y = random.randint(0, 99)

    def getcorrect(self):
        return self.y % self.mod

    def getprompt(self):
        return "%s %% %s" % (self.y, self.mod)


class mod7(mod4):
    name = "modulo 7"
    mod = 7

    def setup(self):
        self.y = random.randint(0, 125)


class trunc4(mathtest):
    name = "truncated division by 4"

    def setup(self):
        self.y = random.randint(1, 99)

    def getcorrect(self):
        return self.y // 4

    def getprompt(self):
        return "%s // 4" % self.y

class trunc4p4(trunc4):
    name = "x // 4 + x"

    def getcorrect(self):
        return (self.y // 4) + self.y

    def getprompt(self):
        return "(%s // 4) + %s" % ((self.y,) * 2)

class monthc(mathtest):
    name = "month code for year calc"

    codes = {
        1: ('Jan', 6),
        2: ('Feb', 2),
        3: ('March', 2),
        4: ('April', 5),
        5: ('May', 0),
        6: ('June', 3),
        7: ('July', 5),
        8: ('August', 1),
        9: ('Sept', 4),
        10: ('Oct', 6),
        11: ('Nov', 2),
        12: ('Dec', 4)
    }

    def setup(self):
        self.month = random.randint(1,12)
        self.year = random.randint(1900,2099)

    def getcorrect(self):
        return self.codes[self.month][1] - int(self.year % 4 == 0 and self.month in (1,2))

    def getprompt(self):
        return "%s, %s" % (self.codes[self.month][0], self.year)


class day(monthc, ycode):
    
    name = "day of week calculations"
    hint = None

    @staticmethod
    def random_date(start, end):
        """
        This function will return a random datetime between two datetime 
        objects.
        """
        from random import randrange
        from datetime import timedelta, datetime

        delta = end - start
        int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
        random_second = randrange(int_delta)
        return (start + timedelta(seconds=random_second))


    def setup(self):
        from datetime import datetime
        self.date = self.random_date(datetime(1900,1,1), datetime(2099,12,31)).date()

    def getcorrect(self):
        return self.date.isoweekday()

    def explicate(self):
        parts = self.calc_year_code(self.date.year)
        month = self.codes[self.date.month]
        ans = ((parts[0] + month[1] + self.date.day) % 7, self.date.isoweekday())
        wdays = ('Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')
        return """
%s
%s // 4 == %s
%s + %s == %s
%s %% 7 == %s
+ %s = %s
+ monthcode(%s) = %s
+ day = %s
+= %s
= %s :== %s
%s
"""     %   (parts[0], 
             parts[0], parts[1], 
             parts[1], parts[0], parts[2], 
             parts[2], parts[3],
             parts[4], parts[5],
             self.date.month, month,
             self.date.day,
             parts[0] + month[1] + self.date.day,
             ans[0], ans[1],
             wdays[ans[1]])

    def getprompt(self):
        return self.date.isoformat()

