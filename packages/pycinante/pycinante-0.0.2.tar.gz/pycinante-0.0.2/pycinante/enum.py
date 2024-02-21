"""This module provides functionality for enum-related operations.
"""

from enum import Enum
from typing import Type, List, Any, Tuple

__all__ = [
    'enum_of',
    'enum_names',
    'enum_values',
    'enum_items'
]

def enum_of(enum: Type[Enum], value: Any) -> Enum:
    """Return an enum instance from the enum according to its value.

    >>> class MyEnum(Enum): E = 'hello world'
    >>> enum_of(MyEnum, 'hello world')
    <MyEnum.E: 'hello world'>
    """
    for member in enum.__members__.values():
        if member.value == value:
            return member
    raise ValueError(f'Unknown the enum value {value}')

def enum_names(enum: Type[Enum]) -> List[str]:
    """Return the names of the enum members.

    >>> class MyEnum(Enum): E = 'hello world'
    >>> enum_names(MyEnum)
    ['E']
    """
    return list(enum.__members__.keys())

def enum_values(enum: Type[Enum]) -> List[Any]:
    """Return the values of the enum members.

    >>> class MyEnum(Enum): E = 'hello world'
    >>> enum_values(MyEnum)
    ['hello world']
    """
    return [e.value for e in enum.__members__.values()]

def enum_items(enum: Type[Enum]) -> List[Tuple[str, Any]]:
    """Return the items of the enum members.

    >>> class MyEnum(Enum): E = 'hello world'
    >>> enum_items(MyEnum)
    [('E', 'hello world')]
    """
    return [(k, v.value) for k, v in enum.__members__.items()]
