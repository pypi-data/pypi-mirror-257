"""This module provides functionality for a list object accession.
"""

from typing import TypeVar, List, Callable, Union, Collection, Iterator, Any, Iterable

__all__ = [
    'is_equal',
    'arange',
    'unique',
    'wrap',
    'swap',
    'sort',
    'flatten'
]

T = TypeVar('T')

def is_equal(obj: Iterable, other: Iterable) -> bool:
    """Return True if each element of obj and other are equal, False otherwise.

    >>> is_equal(None, None)
    True
    >>> is_equal(None, [1, 2, 3, 4])
    False
    >>> is_equal([1, 2, 3, 4], [1, 2, 3, 4])
    True
    >>> is_equal([1, 2, 3, 4], {1, 2, 3, 4})
    True
    >>> is_equal([4, 5, 6], '456')
    False
    >>> from collections import OrderedDict
    >>> is_equal(OrderedDict.fromkeys(iter([1, 2, 3])).keys(), [1, 2, 3])
    True
    """
    if isinstance(obj, Iterable) and isinstance(other, Iterable):
        if len(obj) != len(other):
            return False
        for a, b in zip(obj, other):
            if a != b:
                return False
        return True
    return obj == other

def arange(start: int = 0, stop: int = None, step: int = 1) -> List[int]:
    """Return a list of numbers between `start` and `stop` inclusive.

    >>> arange(10)
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    >>> arange(1, 10)
    [1, 2, 3, 4, 5, 6, 7, 8, 9]
    >>> arange(49, 200, 40)
    [49, 89, 129, 169]
    """
    return list(range((stop and start) or 0, stop or start, step))

def unique(seq: List[T], key: Callable[[T], bool] = None) -> List[T]:
    """Removes duplicate elements from a list while preserving the order of the rest.

    Args:
        seq (List): list to be removed duplicate elements.
        key (Callable): the value of the optional `key` parameter should be a function
            that takes a single argument and returns a key to test the uniqueness.

    >>> unique([1, 2, 3])
    [1, 2, 3]
    >>> unique([1, 2, 1, 3, 3, 2, 1, 2, 3])
    [1, 2, 3]

    Ref: [1] https://github.com/flaggo/pydu/blob/master/pydu/list.py
    """
    key = key or (lambda e: e)
    unique_seq, seen = list(), set()
    for element in seq:
        if key(element) in seen:
            continue
        unique_seq.append(element)
        seen.add(key(element))
    return unique_seq

def wrap(obj: Union[T, List[T]]) -> List[T]:
    """Use list to wrap the object `obj`, and return it directly if the object is of type
    list; if it is a tuple or iterator, it's converted to list.

    >>> wrap('https://www.baidu.com')
    ['https://www.baidu.com']
    >>> wrap([1, 2, 3])
    [1, 2, 3]
    >>> wrap((1, 2, 3, 2, 1, 2))
    [1, 2, 3, 2, 1, 2]
    >>> wrap(iter({4, 5, 6}))
    [4, 5, 6]
    """
    if isinstance(obj, List):
        return obj
    if isinstance(obj, (Collection, Iterator)) and not isinstance(obj, (str, bytes)):
        return list(obj)
    return [obj]

def swap(seq: List[T], i: int, j: int) -> None:
    """Swap the element of `arr[i]` and `arr[j] in the list `arr`.

    >>> seq = [34, 456, 36, 90, 47]
    >>> swap(seq, 1, 4)
    >>> seq
    [34, 47, 36, 90, 456]
    """
    seq[i], seq[j] = seq[j], seq[i]

def sort(seq: List[T], descending: bool = False) -> List[T]:
    """Sort the list in-place in ascending or descending order and return itself.

    >>> arr = [34, 456, 36, 90, 47, 34, 55, 999, 323]
    >>> sort(seq, False)
    [34, 34, 36, 47, 55, 90, 323, 456, 999]
    >>> sort(seq, True)
    [999, 456, 323, 90, 55, 47, 36, 34, 34]
    """
    seq.sort(reverse=descending)
    return seq

def flatten(seq: List[Any]) -> List[T]:
    """Generate each element of the given `seq`. If the element is iterable and is not
    string, it yields each sub-element of the element recursively.

    >>> flatten([])
    []
    >>> flatten([1, 2, 3])
    [1, 2, 3]
    >>> flatten([0, [1, 2, 3], [4, 5, 6], [7, [8, [9]]]])
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    Ref: [1] https://github.com/flaggo/pydu/blob/master/pydu/list.py
    """
    flatten_seq = []
    for element in seq:
        if isinstance(element, Iterable) and not isinstance(element, (str, bytes)):
            for sub in flatten(element):
                flatten_seq.append(sub)
        else:
            flatten_seq.append(element)
    return flatten_seq
