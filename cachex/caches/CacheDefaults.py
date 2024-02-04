# -*- coding: utf-8 -*-


import threading, time, random

from .AbstractCacheDefaults import AbstractCacheDefaults


# Cache configuration defaults.

class CacheDefaults(AbstractCacheDefaults):
	"""Caches defaults."""

	# Default cache arguments.

	def__maxsize = 128
	def__ttl = 600
	def__ttu = lambda key, value, time: time + 600

	# Protected defaults.

	# Default lock class or factory.
	# Specify False|None if you do not want integrated locking capabilities.
	def___lock_class = threading.RLock
