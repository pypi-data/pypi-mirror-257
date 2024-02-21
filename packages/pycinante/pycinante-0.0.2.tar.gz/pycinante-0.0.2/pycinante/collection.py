"""This module provides functionality for working with collections.
"""

import copy
from typing import *

__all__ = [
    'is_empty',
    'is_not_empty',
    'is_collection',
    'deepcopy',
    'percolate',
    'apply',
    'contains',
]

T = TypeVar('T')
U = TypeVar('U')

def is_empty(arr: Collection[T]) -> bool:
    """Return True if the array is empty, False otherwise."""
    return arr is None or len(arr) == 0

def is_not_empty(arr: Collection[T]) -> bool:
    """Return True if the array is not empty, False otherwise."""
    return arr is not None or len(arr) != 0

def is_collection(obj: Any) -> bool:
    """Return True if the object is a collection, False otherwise."""
    return isinstance(obj, Collection)

def deepcopy(arr: Collection[T]) -> Collection[T]:
    """Return an array deep copy of the array `arr`."""
    return copy.deepcopy(arr)

# noinspection PyArgumentList
def percolate(apply: Callable[[T], bool], arr: Collection[T]) -> Collection[T]:
    """Filter existing array elements by the filter `apply`."""
    return type(arr)(filter(apply, arr))

# noinspection PyArgumentList
def apply(apply: Callable[[T], U], arr: Collection[T]) -> Collection[U]:
    """Process existing array elements by the mapper `apply`."""
    return type(arr)(map(apply, arr))

def contains(item: T, arr: Collection[T]) -> bool:
    """Return True if the item is present in the array `arr`, False otherwise."""
    return item in arr
