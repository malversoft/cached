# -*- coding: utf-8 -*-


from .. import cachetools


class NoCache(cachetools.Cache):
	"""Dummy cache implementation that does not cache."""
	def __init__(self, getsizeof=None):
		super().__init__(maxsize=0, getsizeof=getsizeof)
	def __setitem__(self, key, value):
		pass
	def __getitem__(self, key):
		return self.__missing__(key)
	def __contains__(self, key):
		return False
