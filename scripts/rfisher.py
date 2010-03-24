#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# compare head-on between brentp's fisher and R's fisher 

import fisher
import rpy2.robjects as ro

N = 1000

# found these tests on this ticket. (thanks).
# http://projects.scipy.org/scipy/ticket/956
# these values were taken from R as a means to test the code in that ticket.
tablist = [
        ([[100, 2], [1000, 5]], (2.505583993422285e-001,  1.300759363430016e-001)),
        ([[2, 100], [5, 1000]], (2.505583993422285e-001,  1.300759363430016e-001)),
        ([[2, 7], [8, 2]], (8.586235135736206e-002,  2.301413756522114e-002)),
        ([[5, 1], [10, 10]], (4.725646047336584e+000,  1.973244147157190e-001)),
        ([[5, 15], [20, 20]], (3.394396617440852e-001,  9.580440012477637e-002)),
        ([[5, 16], [20, 25]], (3.960558326183334e-001,  1.725864953812994e-001)),
        ([[10, 5], [10, 1]], (2.116112781158483e-001,  1.973244147157190e-001)),
        ([[10, 5], [10, 0]], (0.000000000000000e+000,  6.126482213438734e-002)),
        ([[5, 0], [1, 4]], ('inf',  4.761904761904762e-002)),
        ([[0, 5], [1, 4]], (0.000000000000000e+000,  1.000000000000000e+000)),
        ([[5, 1], [0, 4]], ('inf',  4.761904761904758e-002)),
        ([[0, 1], [3, 2]], (0.000000000000000e+000,  1.000000000000000e+000))
        ]

def rfisher(a, b, c, d):
    v = ro.IntVector([a, b, c, d])
    m = ro.r['matrix'](v, 2, 2)
    s = ro.r['fisher.test'](m)
    return s[0][0] # p.value


def test_rfisher(func):
    for table, ab in tablist:
        p = func(table[0][0], table[0][1], table[1][0], table[1][1])
        print table, p
        assert abs(p - ab[1]) < 0.1, (table, ab, p)


def test_fisher(func):
    for table, ab in tablist:
        p = func(table[0][0], table[0][1], table[1][0], table[1][1])
        print table, p
        assert abs(p.two_tail - ab[1]) < 0.1, (table, ab, p)

def test_speed(f):
    def timed_f(*args, **kwargs):
        import time
        t = time.time()
        f(*args, **kwargs)
        t = time.time() - t
        print >>sys.stderr, "iterations/sec:", float(N)/t
    return timed_f
    
@test_speed
def test_fisher_speed(func):
    for i in range(N):
        p = func(160, 40, 60, 404)

@test_speed
def test_r_speed():
    r_cmd = "m = matrix(c(160, 40, 60, 404), 2, 2); for (i in 1:%d) {fisher.test(m)}" % N
    from subprocess import Popen 
    p = Popen("echo '%s' | R --vanilla --slave" % r_cmd, shell=True)
    #p = Popen("echo 'm=c(1)' | R --vanilla --slave", shell=True)
    p.communicate()


if __name__ == '__main__':
    import sys
    print >>sys.stderr, "calling python fisher..."
    func = fisher.pvalue
    test_fisher(func)
    test_fisher_speed(func)

    print >>sys.stderr, "calling rpy fisher..."
    func = rfisher
    test_rfisher(func)
    test_fisher_speed(func)

    print >>sys.stderr, "calling R directly..."
    test_r_speed()

