# -*- coding: utf-8 -*-


from .DecoratorHelper import DecoratorHelper
from .CacheKeyHelper import CacheKeyHelper


class CacheKeyFunction():
	"""Cache key function builder."""

	def __new__(cls, funcdef, config):
		"""Build cache key function."""

		# Compatibility with cachetools 'key' argument.
		typed = config.typed
		key = None
		if config.key:
			# Alternate key functions can be used.
			alttyped = CacheKeyHelper.get_typed_from_key(config.key)
			if alttyped is not None:
				# Recognized cachetools key function.
				# Resulting 'typed' value prevails over the one specified in decorator parameters.
				typed = alttyped
			else:
				# Alternate key function specified. Will use that.
				key = config.key

		if key is None:
			# Normal case.
			# Key function based on 'typed' parameter.
			key = CacheKeyHelper.get_key_from_typed(typed)

		# Determine key wrapper.
		if funcdef.isunboundmethod or funcdef.isboundmethod:
			# Bound or unbound method.

			if config.stateful:
				# Hash method arguments with object state.

				if callable(config.stateful):
					# Use provided function to get object state.
					if not DecoratorHelper.has_args(config.stateful):
						raise ValueError('Object state getter must accept object as argument: %s.' % (DecoratorHelper.accessor_name(config.stateful),))
					getstate = config.stateful
				else:
					# Try to get object state.
					# Exclude attribute currently used to store caches.
					attr_cache_name = DecoratorHelper.defaults._attr_cache
					getstate = lambda obj: CacheKeyHelper.get_obj_state(obj, attr_cache_name)

				def key_func(*args, **kwargs):
					obj, *args = args				# Get the 'self' or 'cls' method argument.
					args = (getstate(obj), *args)	# Include hashable object state in key.
					return key(*CacheKeyHelper.make_items_hashable(args), **CacheKeyHelper.make_items_hashable(kwargs))

			else:
				# Hash method arguments without object argument.

				def key_func(*args, **kwargs):
					args = args[1:]					# Strip the 'self' or 'cls' method argument.
					return key(*CacheKeyHelper.make_items_hashable(args), **CacheKeyHelper.make_items_hashable(kwargs))

		else:
			# Hash function call.

			def key_func(*args, **kwargs):
				return key(*CacheKeyHelper.make_items_hashable(args), **CacheKeyHelper.make_items_hashable(kwargs))

		return key_func
