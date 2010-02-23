Fisher's Exact Test
===================

Simple, fast implementation of fisher's exact test. Accepts 4 values corresponding
to the 2*2 contingency table. Returns left, right, and 2 tailed p-values
::

    >>> from fisher import pvalue
    >>> mat = [[12, 5], [29, 2]]
    >>> left_tail, right_tail, two_tail = pvalue(12, 5, 29, 2)
    >>> left_tail, right_tail, two_tail
    (0.044554737835078267, 0.99452520602190897, 0.08026855207410688)

