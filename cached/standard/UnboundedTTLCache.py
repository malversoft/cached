# -*- coding: utf-8 -*-


import time

from .. import cachetools


class UnboundedTTLCache(cachetools.TTLCache):
	"""Unbounded cache implementation with per-item time-to-live (TTL) value."""
	def __init__(self, ttl, timer=time.monotonic, getsizeof=None):
		if ttl is None:
			ttl = float('inf')
		super().__init__(maxsize=float('inf'), ttl=ttl, timer=timer, getsizeof=getsizeof)
