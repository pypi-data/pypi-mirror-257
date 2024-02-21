"""This module provides functions to validate a given values.
"""

import re
import numpy as np
from functools import wraps
from typing import *

T = TypeVar('T')
U = TypeVar('U')
Number = Union[int, float]

__all__ = [
    'is_equal',
    'is_empty',
    'is_not_empty',
    'where',
    'require_not_empty',
    'require_gt',
    'require_gt_0',
    'require_ge',
    'require_lt',
    'require_le',
    'require_eq',
    'require_between',
    'require_probability',
    'require_regex',
    'require_variable_name',
    'require_not_none',
    'require_not_none_else',
    'require_not_empty_else',
    'require_type',
    'require_optional_type',
    'check_condition',
    'check_positional_arguments',
    'check_not_empty',
    'check_gt',
    'check_gt_0',
    'check_ge',
    'check_lt',
    'check_le',
    'check_eq',
    'check_between',
    'check_probability',
    'check_regex',
    'check_variable_name',
    'check_not_none',
    'check_not_none_else',
    'check_not_empty_else',
    'check_type',
    'check_optional_type'
]

def is_equal(obj: Any, other: Any, epsilon=1e-6) -> bool:
    """Return whether the object `obj` is equal to the `other`."""
    if isinstance(obj, (int, float)) and isinstance(other, (int, float)):
        return np.abs(obj - other) < epsilon
    return obj == other

def is_empty(obj: Any) -> bool:
    """Return whether the object `obj` is empty."""
    if obj is None:
        return True
    if isinstance(obj, Sized):
        return len(obj) == 0
    if getattr(obj, 'is_empty', None) is not None:
        return getattr(obj, 'is_empty')()
    return False

def is_not_empty(obj: Any) -> bool:
    """Return whether the object `obj` is not empty."""
    return not is_empty(obj)

def where(condition: bool, obj: T, other: U) -> Union[T, U]:
    """Return the first object if the condition is True otherwise return the second."""
    return obj if condition else other

def require_not_empty(obj: T, msg: str = None) -> T:
    """Check whether the object `obj` is not empty."""
    msg = require_not_none_else(msg, 'the obj must be not empty')
    assert is_not_empty(obj), msg
    return obj

def require_gt(val: Number, min_val: Number, msg: str = None) -> Number:
    """Check whether the `val` is greater than the value `min_val`."""
    msg = require_not_none_else(msg, f'the value {val} must be greater than {min_val}')
    assert val > min_val, msg
    return val

def require_gt_0(val: Number, msg: str = None) -> Number:
    """Check whether the `val` is greater than the value 0."""
    msg = require_not_none_else(msg, f'the value {val} must be greater than 0')
    assert val > 0., msg
    return val

def require_ge(val: Number, min_val: Number, msg: str = None) -> Number:
    """Check whether the `val` is greater than or equal to the value `min_val`."""
    msg = require_not_none_else(msg, f'the value {val} must be greater than or equal to {min_val}')
    assert val > min_val or is_equal(val, min_val), msg
    return val

def require_lt(val: Number, max_val: Number, msg: str = None) -> Number:
    """Check whether the `val` is less than the value `max_val`."""
    msg = require_not_none_else(msg, f'the value {val} must be less than {max_val}')
    assert val < max_val, msg
    return val

def require_le(val: Number, max_val: Number, msg: str = None) -> Number:
    """Check whether the `val` is less than or equal to the value `max_val`."""
    msg = require_not_none_else(msg, f'the value {val} must be less than or equal to {max_val}')
    assert val < max_val or is_equal(val, max_val), msg
    return val

def require_eq(val: Number, eq_val: Number, msg: str = None) -> Number:
    """Check whether the `val` is equal to the value `eq_val`."""
    msg = require_not_none_else(msg, f'the value {val} must be equal to {eq_val}')
    assert is_equal(val, eq_val), msg
    return val

def require_between(val: Number, min_val: Number = -np.inf, max_val: Number = np.inf, msg: str = None) -> Number:
    """Check whether the value `val` is in the range `min_val` (included) and `max_val` (included)."""
    msg = require_not_none_else(msg, f'the value {val} must be between {min_val} and {max_val}')
    assert min_val < val < max_val or is_equal(val, min_val) or is_equal(val, max_val), msg
    return val

def require_probability(val: Number, msg: str = None) -> Number:
    """Check whether the value `val` is between 0. and 1."""
    msg = require_not_none_else(msg, f'the probability value {val} must be between 0. and 1.')
    return require_between(val, 0, 1, msg)

def require_regex(val: str, pattern: str, msg: str = None) -> str:
    """Check whether the string `val` matches the regular expression."""
    msg = require_not_none_else(msg, f'the string {val} is not matching the regular expression {pattern}')
    assert re.match(pattern, val), msg
    return val

def require_variable_name(val: str, msg: str = None) -> str:
    """Check whether the variable name `val` is a valid variable name."""
    msg = require_not_none_else(msg, f'the variable {val} is not a valid variable name')
    return require_regex(val, r'^[a-zA-Z_][a-zA-Z0-9_]*$', msg)

def require_not_none(obj: T, msg: str = None) -> T:
    """Check whether the `obj` is not none."""
    msg = require_not_none_else(msg, f'the obj must be not None')
    assert obj is not None, msg
    return obj

def require_not_none_else(obj: T, other: U) -> Union[T, U]:
    """Return the `obj` if the `obj` is not None otherwise return the `other`."""
    return obj if obj is not None else other

def require_not_empty_else(obj: T, other: U) -> Union[T, U]:
    """Return the `obj` if the `obj` is not empty otherwise return the `other`."""
    return obj if is_not_empty(obj) else other

def require_type(obj: T, types: Union[Type, Tuple[Type]], msg: str = None) -> T:
    """Check whether the `obj` is an instance of the `types` type."""
    msg = require_not_none_else(msg, f'the type of `obj` must be the type {types}')
    assert isinstance(obj, types), msg
    return obj

def require_optional_type(obj: Optional[T], types: Union[Type, Tuple[Type]], msg: str = None) -> Optional[T]:
    """Check whether the `obj` is an instance of the `types` type or None."""
    msg = require_not_none_else(msg, f'the type of `obj` must be the type {types} or None')
    assert obj is None or isinstance(obj, types), msg
    return obj

def check_condition(condition: Union[bool, Callable[[], None]], msg: str = None) -> Callable:
    """Check whether the condition is supported.

    Args:
        condition (bool, Callable): boolean condition or a predictor.
        msg (str, optional): error message.
    """
    if isinstance(condition, Callable):
        condition = condition()
    msg = msg or 'the condition is not supported'

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            assert condition, msg
            return func(*args, **kwargs)
        return wrapper
    return decorator

def check_positional_arguments(validator: Callable, index: Union[int, List[int], Callable], **params) -> Callable:
    """Check whether an argument at specified position on the function list is valid.

    Args:
        index (int, List[int], Callable): specifies the index of the argument being checked when the
        type of the index is int or List[int]; Otherwise it represents the decorated function and in
        which case the default index of the argument being checked is 0.
        params (dict): the parameters of the validator to be called.
    """
    # the default index of the argument being checked is 0
    index = require_not_none_else(index, [0])
    indexes = where(isinstance(index, Callable), [0],
                    (isinstance(index, int) and [index] or index))

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            return func(*[validator(args[i], **params) for i in indexes], **kwargs)
        return wrapper

    if isinstance(index, Callable):
        # for annotation without arguments
        return decorator(index)
    return decorator

def check_not_empty(index: Union[int, List[int], Callable] = None, msg: str = None) -> Callable:
    """Check whether the arguments args[index] is not empty."""
    return check_positional_arguments(require_not_empty, index, msg=msg)

def check_gt(min_val: int, index: Union[int, List[int], Callable] = None, msg: str = None) -> Callable:
    """Check whether the args[index] is greater than the value `min_val`."""
    return check_positional_arguments(require_gt, index, min_val=min_val, msg=msg)

def check_gt_0(index: Union[int, List[int]] = None, msg: str = None) -> Callable:
    """Check whether the argument args[index] is greater than the value 0."""
    return check_positional_arguments(require_gt_0, index, msg=msg)

def check_ge(min_val: int, index: Union[int, List[int], Callable] = None, msg: str = None) -> Callable:
    """Check whether the args[index] is greater than or equal to the value `min_val`."""
    return check_positional_arguments(require_ge, index, min_val=min_val, msg=msg)

def check_lt(max_val: int, index: Union[int, List[int], Callable] = None, msg: str = None) -> Callable:
    """Check whether the args[index] is less than the value `max_val`."""
    return check_positional_arguments(require_lt, index, max_val=max_val, msg=msg)

def check_le(max_val: int, index: Union[int, List[int], Callable] = None, msg: str = None) -> Callable:
    """Check whether the args[index] is less than or equal to the value `max_val`."""
    return check_positional_arguments(require_le, index, max_val=max_val, msg=msg)

def check_eq(eq_val: int, index: Union[int, List[int], Callable] = None, msg: str = None) -> Callable:
    """Check whether the args[index] is equal to the value `eq_val`."""
    return check_positional_arguments(require_eq, index, eq_val=eq_val, msg=msg)

def check_between(min_val: int, max_val: int, index: Union[int, List[int], Callable] = None, msg: str = None) -> Callable:
    """Check whether the value args[index] is in the range `min_val` and `max_val`."""
    return check_positional_arguments(require_between, index, min_val=min_val, max_val=max_val, msg=msg)

def check_probability(index: Union[int, List[int]] = None, msg: str = None) -> Callable:
    """Check whether the argument args[index] is between 0. and 1."""
    return check_positional_arguments(require_probability, index, msg=msg)

def check_regex(pattern: str, index: Union[int, List[int]] = None, msg: str = None) -> Callable:
    """Check whether the string `args[index] matches the regular expression."""
    return check_positional_arguments(require_regex, index, pattern=pattern, msg=msg)

def check_variable_name(index: Union[int, List[int], Callable] = None, msg: str = None) -> Callable:
    """Check whether the arguments args[index] is a valid variable name."""
    return check_positional_arguments(require_variable_name, index, msg=msg)

def check_not_none(index: Union[int, List[int], Callable] = None, msg: str = None) -> Callable:
    """Check whether the argument args[index] is not None."""
    return check_positional_arguments(require_not_none, index, msg=msg)

def check_not_none_else(other: int, index: Union[int, List[int], Callable] = None, msg: str = None) -> Callable:
    """Return the args[index] if the args[index] is not None otherwise return the `other`."""
    return check_positional_arguments(require_not_none_else, index, other=other, msg=msg)

def check_not_empty_else(other: int, index: Union[int, List[int], Callable] = None, msg: str = None) -> Callable:
    """Return the args[index] if the args[index] is not empty otherwise return the `other`."""
    return check_positional_arguments(require_not_empty_else, index, other=other, msg=msg)

def check_type(types: Union[Type, Tuple[Type]], index: Union[int, List[int], Callable] = None, msg: str = None) -> Callable:
    """Check whether the args[index] is an instance of the `types` type."""
    return check_positional_arguments(require_type, index, types=types, msg=msg)

def check_optional_type(types: Union[Type, Tuple[Type]], msg: str = None) -> Callable:
    """Check whether the `obj` is an instance of the `types` type or None."""
    return check_positional_arguments(require_optional_type, index, types=types, msg=msg)
