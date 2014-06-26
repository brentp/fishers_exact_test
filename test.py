import fisher

r = fisher.pvalue(94, 48, 3577, 16988)
assert 1e-37 < r.two_tail < 1e-36, r
