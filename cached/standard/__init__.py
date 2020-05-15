# -*- coding: utf-8 -*-
"""Standard mutable mapping classes."""


import sys

from ..caches.Helper import Helper

this_module = sys.modules[__name__]

from .. import cachetools
Helper.with_module_cache_classes(cachetools, lambda kls: setattr(this_module, kls.__name__, kls))

# dict = dict
# from weakref import WeakValueDictionary

from .NoCache import NoCache
from .UnboundedCache import UnboundedCache
from .UnboundedTTLCache import UnboundedTTLCache

__all__ = []
Helper.with_module_cache_classes(this_module, lambda kls: __all__.append(kls.__name__))

del sys, Helper, cachetools
