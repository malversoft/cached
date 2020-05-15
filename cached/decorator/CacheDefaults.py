# -*- coding: utf-8 -*-


from .. import caches


class CacheDefaults(type(caches.defaults)):
	"""Decorator defaults."""

	# Default decorators arguments.

	# Emulate Python @functools.lru_cache() defaults.
	default_maxsize__None = float('inf')
	default_typed = False

	default_exceptions = None
	default_stateful = False
	default_shared = True

	# Protected defaults.

	# Default cache class.
	# Specify None if you do not want cache by default.
	default__cache_class = caches.LRUCache

	# Object attribute used to store per-instance caches.
	# Note: It must begin with double underscore to avoid conflicts if same method is cached at several inheritance levels.
	default__attr_cache = '__caches'

	# List of argument names used to identify unbound methods.
	default__arg_self = ['self']
