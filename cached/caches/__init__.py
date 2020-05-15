# -*- coding: utf-8 -*-
"""Memoizing cache classes."""


import sys

from .Helper import Helper


# Setup module as caches pool.
this_module = sys.modules[__name__]
Helper.setup_pool(this_module)

# Expose all properties and methods a pool has.
__all__ = list(this_module.add().__dict__)

# Convert and expose all cache classes.
from .. import standard
Helper.with_module_cache_classes(standard, (
	add,
	lambda kls: __all__.append(kls.__name__),
))

del sys, Helper, this_module, standard
