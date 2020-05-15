# -*- coding: utf-8 -*-


from collections import OrderedDict


class CacheDescription(OrderedDict):
	"""
	Cache descriptions hold a cache object specification that can be reused
	to instantiate independent cache objects.
	"""

	_class_key = '__class__'

	def __init__(self, kls, params):
		self[self._class_key] = kls
		self.update(params)

	@classmethod
	def from_instance(cls, cache):
		return cls(type(cache), cache.configuration)

	def instantiate(self):
		params = OrderedDict(self)
		kls = params.pop(self._class_key)
		return kls(**params)
