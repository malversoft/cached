# -*- coding: utf-8 -*-


import threading, time, random

from .AbstractCacheDefaults import AbstractCacheDefaults


# Cache configuration defaults.

class CacheDefaults(AbstractCacheDefaults):
	"""Caches defaults."""

	# Default cache arguments.

	default_maxsize = 128
	default_ttl = 600

	# Protected defaults.

	# Default lock class or factory.
	# Specify False|None if you do not want integrated locking capabilities.
	default__lock_class = threading.RLock
