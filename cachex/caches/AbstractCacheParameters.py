# -*- coding: utf-8 -*-


import inspect
from collections import OrderedDict


# Abstract class that 

class AbstractCacheParameters(OrderedDict):
	"""Abstract class to manage functions parameters."""

	_defaults = None

	def __init__(self, params = {}, defaults = {}):
		# Stores a dictionary of parameters setting defaults if necessary.
		# Class defaults have priority over passed defaults.
		for p in params:
			if params[p] is inspect._empty:
				# Missing parameter.
				default = getattr(self._defaults, p, defaults.get(p, inspect._empty))	# Default for missing value.
				if default is not inspect._empty:
					self[p] = default
				else:
					self[p] = None
			elif params[p] is None:
				# Parameter with explicit None value.
				default = getattr(self._defaults, p, defaults.get(p, inspect._empty))	# Default for missing value.
				default_None = getattr(self._defaults, p + self._defaults._suffix_None, default)  # Default for None value.
				if default_None is not inspect._empty:
					self[p] = default_None
				else:
					self[p] = None
			else:
				self[p] = params[p]

	def __getattr__(self, key):
		try:
			return self[key]
		except KeyError:
			raise AttributeError("{!r} object has no attribute {!r}.".format(type(self).__name__, key))

	@classmethod
	def bind(_cls, _func, *args, _strict=False, **kwargs):
		# Given a function and a set of arguments, binds the arguments to the function.
		# Class defaults have priority over function defaults.
		# Intended to select/prepare arguments for a function call.

		params_def = inspect.signature(_func).parameters
		params = OrderedDict()
		defaults = {}
		for p in params_def:
			pd = params_def[p]
			if pd.kind is inspect.Parameter.VAR_POSITIONAL:
				# Skip *args declaration in function.
				continue
			elif pd.kind is inspect.Parameter.VAR_KEYWORD:
				# **kwargs declaration in function will make acceptable any unexpected keyword.
				_strict = False
				continue
			if p in kwargs:
				params[p] = kwargs[p]
				del kwargs[p]
			elif args:
				params[p], *args = args
			else:
				params[p] = inspect._empty
			if params[p] in (None, inspect._empty):
				defaults[p] = pd.default
		if not _strict and kwargs:
			# Include unexpected keyword arguments, if any, to raise TypeError when function is invoked.
			params.update(kwargs)
		# Unexpected positional arguments are dismissed.
		return _cls(params, defaults)
