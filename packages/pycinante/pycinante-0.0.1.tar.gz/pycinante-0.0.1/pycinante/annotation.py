from typing import Callable, Any, Union, List, Type, Tuple, Iterator
from functools import wraps
from validator import (
    where,
    require_not_empty as _require_not_empty,
    require_gt as _require_gt,
    require_gt_0 as _require_gt_0,
    require_ge as _require_ge,
    require_lt as _require_lt,
    require_le as _require_le,
    require_eq as _require_eq,
    require_between as _require_in_range,
    require_probability as _require_probability,
    require_not_none as _require_not_none,
    require_not_none_else as _require_not_none_else,
    require_not_empty_else as _require_not_empty_else,
    require_type as _require_type,
    require_variable_name as _require_variable_name)

__all__ = [
    'require_not_empty',
    'require_gt',
    'require_gt_0',
    'require_ge',
    'require_lt',
    'require_le',
    'require_eq',
    'require_in_range',
    'require_probability',
    'require_variable_name',
    'require_not_none',
    'require_not_none_else',
    'require_not_empty_else',
    'require_type',
]

def to_list(obj):
    if isinstance(obj, List):
        return obj
    if isinstance(obj, (Tuple, Iterator)):
        return list(obj)
    return [obj]

def check_positional_arguments(validator: Callable, index: Union[int, List[int], Callable], **params) -> Callable:
    """Check whether an argument at specified position on the function list is valid.

    Args:
        index (int, List[int], Callable): specifies the index of the argument being checked when the
        type of the index is int or List[int]; Otherwise it represents the decorated function and in
        which case the default index of the argument being checked is 0.
        params (dict): the parameters of the validator to be called.
    """
    # the default index of the argument being checked is 0
    index = _require_not_none_else(index, [0])
    indexes = where(isinstance(index, Callable), [0], to_list(index))

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            for i in indexes:
                validator(args[i], **params)
            return func(*args, **kwargs)
        return wrapper

    if isinstance(index, Callable):
        # for annotation without arguments
        return decorator(index)
    return decorator

def require_not_empty(index: Union[int, List[int], Callable] = None, msg: str = None) -> Callable:
    """Check whether the arguments args[index] is not empty."""
    return check_positional_arguments(_require_not_empty, index, msg=msg)

def require_gt(min_val: int, index: Union[int, List[int], Callable] = None, msg: str = None) -> Callable:
    """Check whether the args[index] is greater than the value `min_val`."""
    return check_positional_arguments(_require_gt, index, min_val=min_val, msg=msg)

def require_gt_0(index: Union[int, List[int]] = None, msg: str = None) -> Callable:
    """Check whether the argument args[index] is greater than the value 0."""
    return check_positional_arguments(_require_gt_0, index, msg=msg)

def require_ge(min_val: int, index: Union[int, List[int], Callable] = None, msg: str = None) -> Callable:
    """Check whether the args[index] is greater than or equal to the value `min_val`."""
    return check_positional_arguments(_require_ge, index, min_val=min_val, msg=msg)

def require_lt(max_val: int, index: Union[int, List[int], Callable] = None, msg: str = None) -> Callable:
    """Check whether the args[index] is less than the value `max_val`."""
    return check_positional_arguments(_require_lt, index, max_val=max_val, msg=msg)

def require_le(max_val: int, index: Union[int, List[int], Callable] = None, msg: str = None) -> Callable:
    """Check whether the args[index] is less than or equal to the value `max_val`."""
    return check_positional_arguments(_require_le, index, max_val=max_val, msg=msg)

def require_eq(eq_val: int, index: Union[int, List[int], Callable] = None, msg: str = None) -> Callable:
    """Check whether the args[index] is equal to the value `eq_val`."""
    return check_positional_arguments(_require_eq, index, eq_val=eq_val, msg=msg)

def require_in_range(min_val: int, max_val: int, index: Union[int, List[int], Callable] = None, msg: str = None) -> Callable:
    """Check whether the value args[index] is in the range `min_val` and `max_val`."""
    return check_positional_arguments(_require_in_range, index, min_val=min_val, max_val=max_val, msg=msg)

def require_probability(index: Union[int, List[int]] = None, msg: str = None) -> Callable:
    """Check whether the argument args[index] is between 0. and 1."""
    return check_positional_arguments(_require_probability, index, msg=msg)

def require_variable_name(index: Union[int, List[int], Callable] = None, msg: str = None) -> Callable:
    """Check whether the arguments args[index] is a valid variable name."""
    return check_positional_arguments(_require_variable_name, index, msg=msg)

def require_not_none(index: Union[int, List[int], Callable] = None, msg: str = None) -> Callable:
    """Check whether the argument args[index] is not None."""
    return check_positional_arguments(_require_not_none, index, msg=msg)

def require_not_none_else(other: int, index: Union[int, List[int], Callable] = None, msg: str = None) -> Callable:
    """Return the args[index] if the args[index] is not None otherwise return the `other`."""
    return check_positional_arguments(_require_not_none_else, index, other=other, msg=msg)

def require_not_empty_else(other: int, index: Union[int, List[int], Callable] = None, msg: str = None) -> Callable:
    """Return the args[index] if the args[index] is not empty otherwise return the `other`."""
    return check_positional_arguments(_require_not_empty_else, index, other=other, msg=msg)

def require_type(types: Union[Type, Tuple[Type]], index: Union[int, List[int], Callable] = None, msg: str = None) -> Callable:
    """Check whether the args[index] is an instance of the `types` type."""
    return check_positional_arguments(_require_type, index, types=types, msg=msg)
