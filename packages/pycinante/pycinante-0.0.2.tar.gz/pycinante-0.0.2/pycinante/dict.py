"""This module provides functionality for a dict-like object operation.
"""

from collections import OrderedDict
from typing import TypeVar, Dict, Callable, Tuple, Union, Optional
from validator import require_variable_name, require_optional_type

__all__ = [
    'is_empty',
    'is_not_empty',
    'update',
    'optional_factory',
    'DefaultDict',
    'AttrDict',
    'attrify',
    'OrderedDict'
]

K = TypeVar('K')
V = TypeVar('V')

def is_empty(d: dict) -> bool:
    """Return True if the dict is empty, False otherwise.

    >>> assert is_empty(None)
    >>> assert is_empty({})
    >>> assert not is_empty({'a': 1, 'b': 2})
    """
    return d is None or len(d.keys()) == 0

def is_not_empty(d: dict) -> bool:
    """Return True if the dict is not empty, False otherwise.

    >>> assert not is_not_empty(None)
    >>> assert not is_not_empty({})
    >>> assert is_not_empty({'a': 1, 'b': 2})
    """
    return d is not None and len(d.keys()) != 0

def update(d: Dict[K, V], m: Dict[K, V] = None, **kwargs) -> Dict[K, V]:
    """Update the dict in place and return itself with new items.

    >>> d = {'a': 1, 'b': 2}
    >>> update(d, {'c': 3, 'd': 4})
    {'a': 1, 'b': 2, 'c': 3, 'd': 4}
    >>> update(d, e=5)
    {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5}
    """
    d.update(m or {}, **kwargs)
    return d

def optional_factory() -> None:
    """Return None rather than raise KeyError if the key is not present in the dict.

    >>> assert optional_factory() is None
    """
    return None

class DefaultDict(Dict[K, V]):
    """A default factory dictionary has default value with default factory. Namely, the default
    will be returned when the key is not present in a dict. But if the factory is None, the key
    error will be raised.

    Args:
        factory (Callable[[], Any]): when a key does not exist in the dictionary, return the
            value returned by the factory method.
        args (Mapping, Iterable): new dictionary initialized from a mapping object's k-v pairs.
        kwargs (Mapping): new dictionary initialized with the name=value pairs.

    >>> d = DefaultDict(optional_factory)
    >>> assert d.get('foo') is None
    >>> d['foo'] = 'bar'
    >>> assert d.get('foo') == 'bar'
    >>> import pickle
    >>> pickle.loads(pickle.dumps(d))
    DefaultFactoryDict(optional_factory, {'foo': 'bar'})
    >>> assert id(d.copy()) != id(d)
    >>> from copy import deepcopy
    >>> assert id(deepcopy(d)) != id(d)

    Ref: [1] https://github.com/flaggo/pydu/blob/master/pydu/dict.py
    """
    def __init__(self, factory: Callable[[], V] = None, *args, **kwargs):
        self.factory = require_optional_type(factory, Callable)
        super(DefaultDict, self).__init__(*args, **kwargs)

    def __getitem__(self, key: K) -> V:
        try:
            return super(DefaultDict, self).__getitem__(key)
        except KeyError:
            return self.__missing__(key)

    def __missing__(self, key: K) -> V:
        if self.factory is None:
            raise KeyError(key)
        self[key] = value = self.factory()
        return value

    def __reduce__(self) -> Tuple:
        args = (self.factory,) if self.factory else ()
        return type(self), args, None, None, iter(self.items())

    def __repr__(self) -> str:
        return (f'DefaultFactoryDict({self.factory.__name__}, '
                f'{super(DefaultDict, self).__repr__()})')

    def __copy__(self) -> 'DefaultDict':
        return self.__class__(self.factory, self)

    def copy(self) -> 'DefaultDict':
        return self.__copy__()

    def __deepcopy__(self, memo) -> 'DefaultDict':
        from copy import deepcopy
        return self.__class__(self.factory, deepcopy(iter(self.items())))

class AttrDict(Dict[str, Union['EasyDict', V]]):
    """An attribute dictionary that allows accessing dictionary values as if accessing class
    attributes. e.g. d['foo'] can be accessed same as d.foo. It requires all key names must
    be valid variable names.

    Args:
        d (Dict[str, Any]): new dictionary initialized from a mapping object's k-v pairs.
        factory (Callable[[], Any]): when a key does not exist in the dictionary, return the
            value returned by the factory method.
        kwargs (Dict[str, Any]): the key-value pairs passed through kwargs will be used together
            with d as the initial dictionary.

    >>> d = AttrDict({'foo': 'bar'})
    >>> assert d['foo'] == d.foo
    >>> d['animal.cat.kitty'] = 'pikachu'
    >>> assert d['animal.cat.kitty'] == d.animal.cat.kitty
    >>> d
    {'foo': 'bar', 'animal': {'cat': {'kitty': 'pikachu'}}}

    Ref: [1] https://github.com/makinacorpus/easydict
         [2] https://flaggo.github.io/pydu/#/zh-cn/dict?id=dictattrdict
    """
    def __init__(self, d: Dict[str, V] = None, factory: Callable = None, **kwargs: Dict[str, V]):
        super(AttrDict, self).__init__()
        self.update(d, **kwargs)
        self.factory = require_optional_type(factory or optional_factory, Callable)
        for key in self.__class__.__dict__.keys():
            if not (key.startswith('__') and key.endswith('__')) and key not in ('update', 'pop'):
                setattr(self, key, getattr(self, key))

    def __setattr__(self, key: str, value: Union['AttrDict', V]) -> None:
        """Set the value associated with the key in the dict."""
        key = require_variable_name(key)
        if isinstance(value, (list, tuple)):
            value = type(value)([(isinstance(e, dict) and self.__class__(e)) or e for e in value])
        elif isinstance(value, dict) and not isinstance(value, AttrDict):
            value = self.__class__(value)
        super(AttrDict, self).__setattr__(key, value)
        super(AttrDict, self).__setitem__(key, value)

    def __setitem__(self, key: str, value: Union['AttrDict', V]) -> None:
        """Set the value associated with the key in the dict. You can use the chain key
        (e.g. k1.k2.k3.k4) to set the value associated with the key `d.k1.k2.k3.k4`.
        """
        keys, obj = key.split('.'), self
        for k in keys[:-1]:
            obj.__setattr__(k, {})
            obj = obj.__getattr__(k)
        obj.__setattr__(keys[-1], value)

    def __getattr__(self, key: str) -> Optional[Union['AttrDict', V]]:
        """Return the value associated with the key from the dict."""
        try:
            return super(AttrDict, self).__getitem__(key)
        except KeyError:
            return self.__missing__(key)

    def __getitem__(self, key: str) -> Optional[Union['AttrDict', V]]:
        """Return the value associated with the key from the dict. You can use the chain key
        (e.g. k1.k2.k3.k4) to get the value associated the key `d.k1.k2.k3.k4`.
        """
        value = self
        for k in key.split('.'):
            assert value is not None and isinstance(value, AttrDict), \
                f'the key {key} is not a valid key'
            value = value.__getattr__(k)
        return value

    def __missing__(self, key: str) -> V:
        if self.factory is None:
            raise KeyError(key)
        self[key] = value = self.factory()
        return value

    def update(self, d: Dict[str, V] = None, **kwargs: Dict[str, V]) -> None:
        """Update the dictionary with the key/value pairs from other, overwriting existing keys."""
        for key, value in update(d or {}, kwargs).items():
            self.__setattr__(key, value)

    def pop(self, key: str, default: V = None) -> Optional[Union['AttrDict', V]]:
        """Remove and return an arbitrary element from the set."""
        delattr(self, key)
        return super(AttrDict, self).pop(key, default)

    def __repr__(self) -> str:
        return '{' + ', '.join([f'{k.__repr__()}: {v.__repr__()}'
                                for k, v in self.items()
                                if k not in ('factory',)]) + '}'

def attrify(d: Dict[str, V], factory: Callable = None, **kwargs) -> AttrDict[V]:
    """Return an object of type AttrDict, which encapsulates the dictionary object d and the
    key-value pairs from kwargs.

    >>> d = attrify({'a': 1, 'b': {'c': [1, 2, 3]}})
    >>> assert d.b.c[2] == 3

    Ref: [1] https://github.com/flaggo/pydu/blob/master/pydu/dict.py
    """
    return AttrDict(d, factory, **kwargs)
