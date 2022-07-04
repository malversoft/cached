# -*- coding: utf-8 -*-


import math

from .. import caches


class CacheDefaults(type(caches.defaults)):
	"""Decorator defaults."""

	# Default decorators arguments.

	# Emulate Python @functools.lru_cache() defaults.
	def__maxsize__None = math.inf
	def__ttl__None = math.inf
	def__typed = False

	def__exceptions = None
	def__stateful = False
	def__shared = True

	# Protected defaults.

	# Default cache class.
	# Specify None if you do not want cache by default.
	def___cache_class = caches.LRUCache

	# Object attribute used to store per-instance caches.
	# Note: It must begin with double underscore to avoid conflicts if same method is cached at several inheritance levels.
	def___attr_cache = '__caches'

	# List of argument names used to identify unbound methods.
	def___arg_self = ['self']
