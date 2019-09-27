# Fisher\'s Exact Test

[![image](https://travis-ci.org/brentp/fishers_exact_test.svg?branch=master)](https://travis-ci.org/brentp/fishers_exact_test)
[![image](https://img.shields.io/pypi/v/fisher.svg)](https://pypi.org/project/fisher)

Simple, fast implementation of [Fisher\'s exact
test](http://en.wikipedia.org/wiki/Fisher's_exact_test). For example,
for the following table:

|              | Having the property | Not having the property |
| ------------ | ------------------- | ----------------------- |
| Selected     | 12                  | 5                       |
| Not selected | 29                  | 2                       |

Perhaps we are interested in whether there is any difference of property
in selected vs. non-selected groups, then we can do the Fisher\'s exact
test.

## Installation

Within this folder :

    git clone git://github.com/brentp/fishers_exact_test.git
    pip install .

From PyPI :

    pip install fisher

Or install the development version :

    pip install git+git://github.com/brentp/fishers_exact_test.git

## Usage

`fisher.pvalue()` accepts 4 values corresponding to the 2-by-2
contingency table, returns an object with attributes for left_tail,
right_tail, and two_tail p-values :

    >>> from fisher import pvalue
    >>> mat = [[12, 5], [29, 2]]
    >>> p = pvalue(12, 5, 29, 2)
    >>> p.left_tail, p.right_tail, p.two_tail  # doctest: +NORMALIZE_WHITESPACE, +ELLIPSIS
    (0.04455473783507..., 0.994525206021..., 0.0802685520741...)

## Benchmark

A simple benchmark that calls the Fisher\'s exact test 1000 times (in
`scripts/rfisher.py`):

    calling python fisher...
    iterations/sec: 3000.62526381
    calling rpy fisher...
    iterations/sec: 289.225902364
    calling R directly...
    iterations/sec: 244.36542276

So the cython fisher is up to 10 times faster than rpy or R version.
