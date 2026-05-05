from __future__ import absolute_import

from ._version import get_versions
from .cfisher import PValues, pvalue, pvalue_npy, pvalue_population

__all__ = ["PValues", "pvalue", "pvalue_npy", "pvalue_population"]

__version__ = get_versions()['version']
del get_versions
