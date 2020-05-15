# -*- coding: utf-8 -*-


from .AbstractCacheParameters import AbstractCacheParameters
from .CacheDefaults import CacheDefaults


class CacheParameters(AbstractCacheParameters):
	"""Caches parameters."""
	_defaults = CacheDefaults()
