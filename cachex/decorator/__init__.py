# -*- coding: utf-8 -*-
"""Memoizing decorator."""


from .CacheDefaults import CacheDefaults
from .DecoratorBuilder import DecoratorBuilder

from .. import caches


def _build_decorator_structure():
	_func_transformer = lambda func: func
	_fake_classmethod_transformer = lambda func: func
	_fake_classmethod_transformer.isclassmethod = True
	_transformers = (
		('function',     _func_transformer),
		('property',     property),
		('staticmethod', staticmethod),
		('classmethod',  _fake_classmethod_transformer),  # Use fake 'classmethod' transformer instead of Python's.
		                                                  # Decorator will already return a 'classmethod' equivalent.
	)

	_defaultnode = DecoratorBuilder._defaultnode

	# Create root function.
	_root = _defaultnode(_func_transformer)

	# Create transformer-specific leaves.
	for name, transformer in _transformers:
		setattr(_root, name, _defaultnode(transformer))

	# Create cache-specific leaves...
	for method in ('lfu_cache', 'lru_cache', 'ttl_cache', 'rr_cache', 'unbounded_cache', 'shared',):
		_node = getattr(DecoratorBuilder, method)
		# ... in root.
		setattr(_root, method, _node(_func_transformer))
		# ... in transformer leaves.
		for name, transformer in _transformers:
			_leaf = getattr(_root, name)
			setattr(_leaf, method, _node(transformer))

	return _root

cached = _build_decorator_structure()

# Add auxiliar utilities.
cached.defaults = CacheDefaults()
cached.caches = caches

__all__ = ['cached']

del CacheDefaults, DecoratorBuilder, caches, _build_decorator_structure
