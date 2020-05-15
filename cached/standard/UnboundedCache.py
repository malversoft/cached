# -*- coding: utf-8 -*-


from .. import cachetools


class UnboundedCache(cachetools.Cache):
	"""Unbounded cache implementation."""
	def __init__(self, getsizeof=None):
		super().__init__(maxsize=float('inf'), getsizeof=getsizeof)
