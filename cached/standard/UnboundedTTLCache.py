# -*- coding: utf-8 -*-


import time, math

from .. import cachetools


class UnboundedTTLCache(cachetools.TTLCache):
	"""Unbounded cache implementation with per-item time-to-live (TTL) value."""
	def __init__(self, ttl, timer=time.monotonic, getsizeof=None):
		super().__init__(maxsize=math.inf, ttl=ttl, timer=timer, getsizeof=getsizeof)
