import sys
import random
import time
from datetime import datetime
import cPickle as pickle
import os.path


log_fname = 'plog.pkl'
xmax = 25
ymax = 13
alphachars = '!#$%&*+0123456789=?@ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxy'

if not os.path.exists(log_fname):
    log = []
else:
    log = pickle.load(open(log_fname))


try:
    while 1:
        correct_points = 0
        rang = random.randint(10, 15)
        for y in xrange(ymax):
            line = ''
            for x in xrange(xmax):
                result = int(bool(random.randint(0,rang)))
                if not result:
                    correct_points += 1
                    nextchar = random.choice(alphachars)
                else:
                    nextchar = ' '

                line += nextchar

            print line


        print "how many points?"
        start = time.time()
        answer = int(sys.stdin.readline().rstrip())
        end = time.time()

        print answer - correct_points
        print
        time.sleep(1)
        log.append((datetime.now(), end - start, answer - correct_points, xmax, ymax, rang))

except KeyboardInterrupt:
    print "exiting..."

finally:
    if log:
        print "saving..."
        pickle.dump(log, open(log_fname, 'wb'))
