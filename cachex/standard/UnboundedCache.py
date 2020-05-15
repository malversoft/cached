# -*- coding: utf-8 -*-


import math

from .. import cachetools


class UnboundedCache(cachetools.Cache):
	"""Unbounded cache implementation."""
	def __init__(self, getsizeof=None):
		super().__init__(maxsize=math.inf, getsizeof=getsizeof)
