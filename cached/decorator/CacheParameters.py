# -*- coding: utf-8 -*-


from .CacheDefaults import CacheDefaults
from ..caches.AbstractCacheParameters import AbstractCacheParameters


class CacheParameters(AbstractCacheParameters):
	"""Decorator parameters."""
	_defaults = CacheDefaults()
