<a id="top"></a>
[@cached] cache classes
=======================

[@cached] allows to extend mutable mapping types, including [cachetools] memoizing classes, to ease using them as caches.

- [Features](#features)
  - [Integrated locking capability](#integrated-locking-capability)
  - [Integrated hit/miss counters](#integrated-hitmiss-counters)
  - [Cache information](#cache-information)
  - [Cloning capability](#cloning-capability)
  - [Conversion of cache classes](#conversion-of-cache-classes)
  - [Pools of cache classes](#pools-of-cache-classes)
  - [Defaults management](#defaults-management)
- [Cache implementations](#cache-implementations)

<br/>

# Features

Apart from the features of mutable mapping types and [cachetools] memoizing classes, [@cached] classes provide several additional features.

<br/>

## Integrated locking capability

Access to caches is not thread-safe per se, but cache classes have by [default] an integrated lock that can be used to define exclusive access contexts.

```python
cache = MyCache()
cache['a'] = 'Item a'
cache['b'] = 'Item b'

# Some thread spawning here.
...

with cache.lock:
    # Exclusive access to cache.
    try:
        print('Values: ', cache['a'], cache['b'])
    except KeyError:
        print('Missing value')
```

This integrated lock can be subtituted by any object that implements the [context manager](https://docs.python.org/library/threading.html#with-locks) protocol, depending on the specific access exclusivity needs.

```python
cache.lock = threading.RLock()
# or
cache.lock = threading.BoundedSemaphore()
# or
cache.lock = threading.Condition()
...
```

To reset to a [default] lock, assign ```True```.

```python
cache.lock = True

with cache.lock:
    # Exclusive access to cache.
    ...
```

To disable integrated locking, assign ```False```.

```python
cache.lock = False

# Context use will not break, so code does not need to be changed.
# It just will not acquire exclusive access.
with cache.lock:
    # Non exclusive access to cache.
    ...

assert(not cache.lock)
```

<br/>

## Integrated hit/miss counters

Cache classes have integrated support for counting hits and misses when accessing the cache.

Due to the duck typing nature of Python this cannot be completely automated, so the developer will have to decide where and how to use these counters. But several ways of easing this are provided.

- Counters can be explicitly incremented specifying when a hit or a miss has occurred.

  ```python
  cache = MyCache()
  cache['a'] = 'Item a'
  cache['b'] = 'Item b'

  for k in ('a', 'b', 'c'):
      try:
          print('Value of %r: %r' % (k, cache[k]))
          cache.did_hit()        # Explicitly increments hits.
      except KeyError:
          print('Missing value: %r' % k)
          cache.did_miss()       # Explicitly increments misses.
  
  assert(cache.hits == 2)
  assert(cache.misses == 1)
  ```

- Alternatively, counters can be enabled to be incremented implicitly when accessing the cache.

  ```python
  cache = MyCache()
  cache['a'] = 'Item a'
  cache['b'] = 'Item b'

  cache.counters_enabled = True

  for k in ('a', 'b', 'c'):
      try:
          print('Value of %r: %r' % (k, cache[k]))
      except KeyError:
          print('Missing value: %r' % k)

  cache.counters_enabled = False

  assert(cache.hits == 2)
  assert(cache.misses == 1)
  ```

  - The easiest way is to use the provided ```counters``` property to enclose a context where the counters will be incremented implicitly.

  ```python
  cache = MyCache()
  cache['a'] = 'Item a'
  cache['b'] = 'Item b'

  with cache.counters:

      for k in ('a', 'b', 'c'):
          try:
              print('Value of %r: %r' % (k, cache[k]))
          except KeyError:
              print('Missing value: %r' % k)
  
  assert(cache.hits == 2)
  assert(cache.misses == 1)
  assert(not cache.counters_enabled)    # Still disabled outside the context.
  ```

  This context can also be used to specify where to NOT implicitly increment these counters.

  ```python
  cache = MyCache()
  cache['a'] = 'Item a'
  cache['b'] = 'Item b'

  cache.counters_enabled = True

  print('Value of a: %r' % cache['a'])

  assert(cache.hits == 1)
  
  with cache.counters(False):
 
      print('Cache contents:')
      for k in cache:
          # Hits will not be automatically incremented.
          print('Value of %r: %r' % (k, cache[k]))

  assert(cache.hits == 1)
  assert(cache.counters_enabled)    # Still enabled outside the context.
  ```

The ```counters``` property can also be used to check if the hit/miss counters are enabled or have ever been incremented, so you can discriminate when to have these counters into account or not at a later point.

```python
if cache.counters:
    print('hits: %r, misses: %r' % (cache.hits, cache.misses))
else:
    print('Cache counters not in use')
```

As seen in the examples, the number of hits and misses registered by the cache can be obtained using he ```hits``` and ```misses``` properties.

The hit/miss counters can be reset at any time.

```python
cache.counters_reset()
# or
cache.clear()      # This also empties the cache.
```

Just as a convenience, the ```counters``` property can also be used as an alternative access to reset the hit/miss counters or to enable/disable its implicit use.

```python
cache.counters.reset()
# is equivalent to
cache.counters_reset()
```
```python
cache.counters.enabled
# is equivalent to
cache.counters_enabled
```

<br/>

## Cache information

The ```parameters``` property provides a dictionary with the parameters used to create the cache, including the unspecified ones that took [default] values. This is for information purposes only, changing the values has no effect.

The ```info``` property provides a named tuple showing hits, misses, maximum size and current size. This helps measuring the efectiveness of the cache and helps tuning its parameters.

Note that hits and misses infomation only has sense if the [integrated cache counters](#integrated-hitmiss-counters) are used.

```python
>>> cache = MyCache(ttl=3600)
>>> 
>>> cache.parameters
{'maxsize': 128, 'ttl': 3600}
>>> 
>>> cache['a'] = 'Item a'
>>> cache.info
CacheInfo(hits=0, misses=0, maxsize=128, currsize=1)
```

Each cache instance also provides a unique hash value. This value does not contain any information about the cache contents.

```python
cache1 = MyCache()
cache2 = MyCache()

assert(hash(cache1) != hash(cache2))
```

<br/>

## Cloning capability

A cache instance can be cloned to get an empty fresh copy of it.

```python
cache1 = MyCache()
cache1['a'] = 'Item a'

cache2 = cache1.clone()

assert(cache1.currsize == 1)
assert(cache2.currsize == 0)

assert(type(cache1) == type(cache2))
assert(cache1.parameters == cache2.parameters)
```

<br/>

## Conversion of cache classes

Any mutable mapping type, including [cachetools] cache classes, can be converted into [@cached] cache classes acquiring all its features while fully preserving backward compatibility.

```python
>>> from cached import caches
>>> from cachetools import Cache     # -> cachetools cache class.
>>> 
>>> Cache = caches.convert(Cache)    # -> @cached cache class.
>>> 
>>> cache = Cache()
>>> cache.info
CacheInfo(hits=0, misses=0, maxsize=128, currsize=0)
```

Even plain ```dict``` and ```weakref.WeakValueDictionary``` types can be converted.

```python
>>> from cached import caches
>>> 
>>> DictCache = caches.convert(dict)
>>> 
>>> cache = DictCache()
>>> cache.info
CacheInfo(hits=0, misses=0, maxsize=None, currsize=0)
```

If you try to convert an already converted class it will not be converted again, you will just get the same class.

__Note__: The conversion consists in providing a wrapper class around the original mutable mapping type. For this reason it is not recommended to develop cache classes inherited from [@cached] classes (if you want to use features like [managed defaults](#defaults-management) or [cloning](#cloning-capability), for example). The prefered method to develop a cache class with [@cached] features is to inherit from a mutable mapping (for example a [cachetools] cache class) and then convert the developed class.

<br/>

## Pools of cache classes

Pools are containers of cache classes that you can organize to conveniently access all your converted cache classes from all over your application.

Meet the [@cached] main pool of cache classes. Some already [implemented cache classes](#cache-implementations) are provided by default in the main pool of classes.

```python
from cached import caches

cache = caches.UnboundedCache()
```

For convenience, any cache class can be added to a pool of classes. This makes the class accessible across modules without having to import or convert it in each module you use it.

If a standard mutable mapping type (for example a [cachetools] cache class) is added to a pool, it will be automatically [converted](#conversion-of-cachetools-classes).

Example:

```python
from cached import caches
from mycaches import MyCache     # -> Mutable mapping class.

caches.add(MyCache)
```

Now the class can be used in other modules without having to import or convert it again.

```python
from cached import caches

cache = caches.MyCache()
cache.info
```

Even entire modules containing mutable mapping classes can be added to the pool to have those classes conveniently converted and accessible.

```python
from cached import caches
import mycaches          # -> Module with mutable mapping classes.

caches.add(mycaches)

cache = caches.mycaches.MyCache()
```

Alternative names can be used to avoid collisions.

```python
# Adding a cache class with alternative name.
caches.add(MyCache, 'OtherCache')

cache = caches.OtherCache()
```
```python
# Adding a module with alternative name.
caches.add(mycaches, 'othercaches')

cache = caches.othercaches.MyCache()
```

When adding a module, the created container is also another pool of classes.

Examples:

```python
from cached import caches

import mycaches
import othercaches
import nestedcaches
from othermodule import MyCache

caches.add(mycaches)
caches.mycaches.add(MyCache)
otherpool = caches.add(othercaches, 'other')
otherpool.add(nestedcaches, 'nested')

assert(caches.mycaches.MyCache)
assert(caches.other.nested)
```

Empty pools can also be added or created to use them at will, set global [defaults], etc. Any structure can be built to conveniently access cache classes.

```python
caches.add('emptypool')
assert(caches.emptypool)

mypool = caches.add()
assert(mypool.defaults)
```

<br/>

## Defaults management

Default parameters for creating cache instances are centralized, global and can be easily accessed and modified using any [pool of cache classes](#pools-of-cache-classes).

```python
>>> from cached import caches
>>> cache1 = caches.MyCache()
>>> cache1.maxsize
128
>>> caches.defaults.maxsize = 1024
>>> cache2 = caches.MyCache()
>>> cache2.maxsize
1024
```

__Note__: The defaults are global by design. Modifying them will affect the defaults for all cache classes in all [pools](#pools-of-cache-classes).

You can create defaults for your own developed cache classes.

Example:

```python
# Create a customized cache class with customized constructor arguments.

import cachetools

class MyCache(cachetools.Cache):

    def __init__(self, maxsize, custom_param):
        self.custom = custom_param
        super().__init__(maxsize=maxsize)

# Add to the pool of caches, for convenience.
from cached import caches
caches.add(MyCache)

# Set a default value for your customized argument.
caches.defaults.custom_param = 'CUSTOM VALUE'
```

Now the class can be instantiated in any module using the default value specified for the parameter.

```python
from cached import caches

cache = caches.MyCache()    # No parameters informed.
print(cache.custom)         # -> 'CUSTOM VALUE'
```

Defaults can also be defined and accessed by name.

```python
caches.defaults['custom_param'] = 'CUSTOM VALUE'
```

Defaults can even be deleted, if you want to get rid of a specific one and force to inform it on object creation.

```python
del caches.defaults.custom_param
# or
del caches.defaults['custom_param']
```

For any given parameter, there is the possibility to define a different default value to use when the parameter is not missing but explicitly set to ```None```. If this is not set, the default value for missing parameter will be used for both cases.

```python
# Default value for missing parameter.
caches.defaults.custom_param

# If set, default for explicit None value.
caches.defaults.custom_param__None
```

You can check the defined defaults at any moment.

```python
>>> from cached import caches
>>> caches.defaults
CacheDefaults({'maxsize': 128, 'ttl': 600})
>>> 'maxsize' in caches.defaults
True
>>> list(caches.defaults)
['maxsize', 'ttl']
>>> dict(caches.defaults)
{'maxsize': 128, 'ttl': 600}
```

There are also some protected defaults. Protected defaults are not shown when defaults are listed but can be modified anyway. Modify them only if you know what you are doing.

```python
# Default lock class or factory for cache objects.
caches.defaults._lock_class
```

<br/>

# Cache implementations

Some cache classes are provided by default in the main [pool of classes](#pools-of-cache-classes).

Please refer to the [cachetools documentation](https://cachetools.readthedocs.io/en/stable/#cache-implementations) for a better understanding of the caches parameters.

- A direct [conversion](#conversion-of-cachetools-classes) of the classes provided by [cachetools].
  
  These are documented in the [cachetools documentation](https://cachetools.readthedocs.io/en/stable/#cache-implementations).
  
- ```python
  class caches.UnboundedCache(getsizeof=None)
  ```

  Unbounded cache that never evicts items and can grow without limit.

- ```python
  class caches.UnboundedTTLCache(ttl, timer=time.monotonic, getsizeof=None)
  ```

  Cache without size limit that evicts items only when their time-to-live expires, and not based on the cache size.

  Refer to the [cachetools documentation](https://cachetools.readthedocs.io/en/stable/#cachetools.TTLCache) for details on the parameters.

- ```python
  class caches.NoCache(getsizeof=None)
  ```

  Implementation of a zero-size cache that does not store items and thus always misses. Not intended to be useful for production use, just for testing and development purposes.

As stated in the section about [converting classes](#conversion-of-cachetools-classes), it is not recommended to develop cache classes inherited from [@cached] classes. The developed classes must inherit from a mutable mapping type (like [cachetools] cache classes), and later be [converted](#conversion-of-cachetools-classes) and optionally added to a [pool](#pools-of-cache-classes).

For this purpose, standard versions of these mutable mapping classes are made available.

```python
from cached import standard, caches
standard.UnboundedTTLCache    # -> Standard mutable mapping class
caches.UnboundedTTLCache      # -> @cached version
```

<br/>

[default]: #defaults-management
[defaults]: #defaults-management
[@cached]: ./README.md#top
[cachetools]: https://github.com/tkem/cachetools/
