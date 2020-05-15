# -*- coding: utf-8 -*-


from collections.abc import Mapping, Iterable

from .. import cachetools

from .DecoratorHelper import DecoratorHelper


# Hashable dictionary implementation.
_hashabledict = type('dict', (dict,), {
	'__module__' : None,
	'__hash__' : lambda self: hash(frozenset(self.items())),
})


class CacheKeyHelper():
	"""Cache key function helper functions."""

	typedkeys = {
		False : 'hashkey',
		True : 'typedkey',
	}

	# Tuple of hashable scalar iterable types, iterables that do not need to hash its items to be hashable.
	# IMPORTANT: If an iterable type can contain a non-hashable item (tuple, for example), it must NOT be in this list.
	hashable_scalar_iterables = (str, bytes)

	@classmethod
	def get_key_from_typed(cls, typed):
		return getattr(cachetools.keys, cls.typedkeys[bool(typed)])

	@classmethod
	def get_typed_from_key(cls, key):
		l = key and list(filter(lambda k: cls.typedkeys[k] == key.__name__, cls.typedkeys))
		return l and l[0] or None

	@classmethod
	def make_obj_hashable(cls, obj):
		if DecoratorHelper.is_cache_instance(obj):
			# Object is cache instance. Hash cache instance, not its elements.
			return obj
		elif isinstance(obj, Mapping):
			# Object is a mapping.
			return _hashabledict(cls.make_items_hashable(obj))
		elif isinstance(obj, Iterable) and not isinstance(obj, cls.hashable_scalar_iterables):
			# Object is a non scalar iterable.
			return tuple(cls.make_items_hashable(obj))
		else:
			# Assume scalar object.
			return obj

	@classmethod
	def make_items_hashable(cls, obj):
		if isinstance(obj, Mapping):
			# Object is a mapping.
			return {k : cls.make_obj_hashable(obj[k]) for k in obj}
		elif isinstance(obj, Iterable) and not isinstance(obj, cls.hashable_scalar_iterables):
			# Object is a non scalar iterable.
			return (cls.make_obj_hashable(o) for o in obj)
		else:
			# Assume scalar object.
			return obj

	@classmethod
	def is_allowed_in_state(cls, obj, key = None):
		return (
			not (key and key.startswith('__') and key.endswith('__')) and	# Filter magic attributes.
			not hasattr(obj, '__get__') and									# Filter function/method/property descriptors.
			not DecoratorHelper.is_cache_instance(obj)						# Filter attributes containing caches.
		)

	@classmethod
	def get_obj_state(cls, obj, attr_cache_name):
		try:
			# Try to retrieve object state.
			getstate = obj.__getstate__
		except AttributeError:
			try:
				# Try to use object attributes as state.
				state = obj.__dict__
			except AttributeError:
				try:
					# Try to use slot properties as state.
					slots = obj.__slots__
				except AttributeError:
					# As last attempt, will use the object itself as state to hash.
					return obj
				else:
					# Using __slots__
					# Try to reduce to a collection of scalar values.
					state = {}
					for k in slots:
						value = getattr(obj, k, None)
						if cls.is_allowed_in_state(value, k):
							state[k] = value
			else:
				# Using __dict__
				state = dict(state)					# Use mutable mapping instead of mapping proxy.
				state.pop(attr_cache_name, None)	# Exclude possible object caches from the state.
				# Try to reduce to a collection of scalar values.
				state = {k : state[k] for k in state if cls.is_allowed_in_state(state[k], k)}
		else:
			# Using __getstate__()
			state = getstate()
			# Try to reduce to a collection of scalar values.
			if isinstance(state, Mapping):
				# State is a mapping.
				state = {k : state[k] for k in state if cls.is_allowed_in_state(state[k], k)}
			elif isinstance(state, Iterable) and not isinstance(state, cls.hashable_scalar_iterables):
				# State is a non scalar iterable.
				state = (o for o in state if cls.is_allowed_in_state(o))
		return state
