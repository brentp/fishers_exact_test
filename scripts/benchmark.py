#!/usr/bin/env python
"""Benchmark fisher vs scipy for scalar and vectorised calls."""

import time
import numpy as np
import fisher
from scipy.stats import fisher_exact

RNG = np.random.default_rng(42)
SIZES = [100, 1_000, 10_000, 100_000]
SCALAR_N = 10_000  # iterations for the scalar benchmark


def _random_tables(n):
    return [RNG.integers(1, 200, size=4, dtype=np.uint32) for _ in range(n)]


def _random_npy_arrays(n):
    data = RNG.integers(1, 200, size=(n, 4), dtype=np.uint32)
    return data[:, 0], data[:, 1], data[:, 2], data[:, 3]


def bench(label, fn, *, repeat=3):
    times = []
    for _ in range(repeat):
        t0 = time.perf_counter()
        fn()
        times.append(time.perf_counter() - t0)
    best = min(times)
    return label, best


def fmt(label, t, n):
    return f"  {label:<45s}  {t*1e3:8.2f} ms  ({n/t:>12,.0f} /s)"


print("=" * 75)
print(f"{'Scalar benchmark':^75}")
print("=" * 75)
tables = _random_tables(SCALAR_N)

label, t = bench(
    f"fisher.pvalue (n={SCALAR_N:,})",
    lambda: [fisher.pvalue(int(a), int(b), int(c), int(d)) for a, b, c, d in tables],
)
print(fmt(label, t, SCALAR_N))

label, t = bench(
    f"scipy.fisher_exact (n={SCALAR_N:,})",
    lambda: [fisher_exact([[int(a), int(b)], [int(c), int(d)]]) for a, b, c, d in tables],
)
print(fmt(label, t, SCALAR_N))

print()
print("=" * 75)
print(f"{'pvalue_npy benchmark':^75}")
print("=" * 75)

for n in SIZES:
    a, b, c, d = _random_npy_arrays(n)

    label, t = bench(
        f"fisher.pvalue_npy          (n={n:>7,})",
        lambda: fisher.pvalue_npy(a, b, c, d),
    )
    print(fmt(label, t, n))

    label, t = bench(
        f"fisher.pvalue loop         (n={n:>7,})",
        lambda: [fisher.pvalue(int(x), int(y), int(u), int(v)) for x, y, u, v in zip(a, b, c, d)],
    )
    print(fmt(label, t, n))

    print()
