"""
Cython Fisher's exact test:
Fisher's exact test is a statistical significance test used in the
analysis of contingency tables where sample sizes are small.

Function lngamma(), lncombination(), hypergeometric_probability(),
were originally written by Oyvind Langsrud:

Oyvind Langsrud
Copyright (C) : All right reserved.
Contact Oyvind Langsrud for permission.

Adapted to Cython version by:
Haibao Tang, Brent Pedersen
"""

#cython: cdivision=True

import numpy as np

cimport numpy as np
cimport cython

cdef extern from "math.h":
    double log(double) nogil
    double exp(double) nogil
    double lgamma(double) nogil

# Setup Numpy C-API
np.import_array()

cdef inline double _naive_lnfactorial(int n) nogil:
    cdef double acc = 0.0
    cdef int i
    for i in range(2, n + 1):
        acc += log(i)
    return acc

# Tabulated ln n! for n \in [0, 1023]
cdef double[:] _lnfactorials1 = np.zeros(1024)
cdef int i
for i in range(1024):
    _lnfactorials1[i] = _naive_lnfactorial(i)


# Logarithm of n! with algorithmic approximation
@cython.boundscheck(False)
cdef inline double lnfactorial(int n) nogil:
    return _lnfactorials1[n] if n < 1024 else lgamma(n + 1)


# Logarithm of the number of combinations of 'n' objects taken 'p' at a time
cdef inline double lncombination(int n, int p) nogil:
    return lnfactorial(n) - lnfactorial(p) - lnfactorial(n - p)


# Compute the hypergeometric probability, or probability that a list of
# 'n' objects should contain 'x' ones with a particular property when the
# list has been selected randomly without replacement from a set of 'N'
# objects in which 'K' exhibit the same property
cdef inline double hypergeometric_probability(int x, int n, int K, int N) nogil:
    return exp(lncombination(K, x)
               + lncombination(N - K, n - x)
               - lncombination(N, n))


cdef class PValues:
    cdef readonly double left_tail
    cdef readonly double right_tail
    cdef readonly double two_tail

    def __cinit__(self, double left_tail, double right_tail, double two_tail):
        self.left_tail = left_tail
        self.right_tail = right_tail
        self.two_tail = two_tail

    def __repr__(self):
        return "PValues(left_tail=%.4g, right_tail=%.4g, two_tail=%.4g)" % \
            (self.left_tail, self.right_tail, self.two_tail)

    # http://docs.cython.org/docs/special_methods.html
    # < 0 | <= 1 | == 2 | != 3 |  > 4 | >= 5
    def __richcmp__(PValues self, double other, int op):
        raise Exception("must compare with one of the attributes"
                        " not the PValues object")


cpdef PValues pvalue(int a_true, int a_false, int b_true, int b_false):
    # Convert the a/b groups to study vs population.
    cdef int k = a_true
    cdef int n = a_false + a_true  # total in study.
    cdef int K = a_true + b_true
    cdef int N = K + a_false + b_false

    cdef int lm = max(0, n - (N - K))
    cdef int um = min(n, K)
    if lm == um:
        return PValues(1.0, 1.0, 1.0)

    cdef double epsilon = 1e-6
    cdef double cutoff = hypergeometric_probability(k, n, K, N)
    cdef double left_tail = 0, right_tail = 0, two_tail = 0
    cdef int i
    cdef double p
    with nogil:
        for x in range(lm, um + 1):
            p = hypergeometric_probability(x, n, K, N)
            if x <= k:
                left_tail += p
            if x >= k:
                right_tail += p

            if p <= cutoff + epsilon:
                two_tail += p

    return PValues(min(left_tail, 1.0),
                   min(right_tail, 1.0),
                   min(two_tail, 1.0))


# k, n = study_true, study_tot,
# K, N = population_true, population_tot
def pvalue_population(int k, int n, int K, int N):
    return pvalue(k, n - k, K - k, N - K - n + k)


@cython.boundscheck(False)
def pvalue_npy(
       np.ndarray[np.uint_t] a_true,
       np.ndarray[np.uint_t] a_false,
       np.ndarray[np.uint_t] b_true,
       np.ndarray[np.uint_t] b_false):

    cdef int shape = a_true.shape[0],
    cdef np.ndarray[np.double_t] lefts = np.zeros(shape, dtype=np.double)
    cdef np.ndarray[np.double_t] rights = np.zeros(shape, dtype=np.double)
    cdef np.ndarray[np.double_t] twos = np.zeros(shape, dtype=np.double)

    cdef int i
    cdef double l, r, t
    cdef PValues p
    for i in range(shape):
        p = pvalue(a_true[i], a_false[i], b_true[i], b_false[i])
        lefts[i] = p.left_tail
        rights[i] = p.right_tail
        twos[i] = p.two_tail
    return lefts, rights, twos
