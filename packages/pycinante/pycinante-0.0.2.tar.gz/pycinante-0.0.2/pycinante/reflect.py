"""This module provides functions to operate a function or class similar to on Java.
"""

import inspect
from functools import reduce
from typing import Any, List, Callable, Tuple, Optional, Type

__all__ = [
    'cinvoke',
    'compose',
    'func_name',
    'func_arguments',
    'is_accept_args',
    'is_accept_varargs',
    'is_accept_kwargs'
]

def cinvoke(c: bool, obj: object, m: str, *args, **kwargs) -> Any:
    """Return obj.m(*args, **kwargs) if c is True, obj otherwise.

    >>> cinvoke(True, 'hello world', 'upper')
    'HELLO WORLD'
    """
    return (c and getattr(obj, m)(*args, **kwargs)) or obj

def compose(*funcs: List[Callable]) -> Callable:
    """Compose all functions. The previous function must accept one argument, which is the
    output of the next function. The last function can accept any args and kwargs.

    compose(f1, f2, f3)(*args, **kwargs) is same to f3(f2(f1(*args, **kwargs))).

    >>> compose(lambda x: x + 10, lambda x: x ** 2, lambda x: x / 0.5)(10)
    800.0
    """
    return reduce(lambda f, g: lambda *args, **kwargs: g(f(*args, **kwargs)), funcs)

def func_name(func: Callable) -> str:
    """Return the name of the function `func`.

    >>> func_name(lambda x: x)
    '<lambda>'
    """
    return func.__name__

def func_arguments(func: Callable) -> Tuple[List, Optional[str], Optional[str], List]:
    """Get the names and default values of a function's parameters.

    A tuple of four things is returned: (args, varargs, keywords, defaults).
    'args' is a list of the argument names, including keyword-only argument names.
    'varargs' and 'keywords' are the names of the * and ** parameters or None.
    'defaults' is an n-tuple of the default values of the last n parameters.

    >>> func_arguments(cinvoke)
    (['c', 'obj', 'm'], None, None, [None, None, None])
    >>> func_arguments(func_arguments)
    (['func'], None, None, [None])

    Ref: [1] https://github.com/flaggo/pydu/blob/master/pydu/inspect.py
    """
    args, var_args, var_kwargs, default = [], None, None, []
    for param in inspect.signature(func).parameters.values():
        if param.kind == inspect.Parameter.POSITIONAL_OR_KEYWORD:
            args.append(param.name)
            default.append(None if param.default is param.empty else param.default)
            if param.kind == inspect.Parameter.VAR_POSITIONAL:
                var_args = param.name
            if param.kind == inspect.Parameter.VAR_KEYWORD:
                var_kwargs = param.name
    return args, var_args, var_kwargs, default

def is_accept_args(func: Callable) -> bool:
    """Return True if the function `func` accepts `args` parameters, False otherwise.

    >>> is_accept_args(lambda: True)
    False
    >>> is_accept_args(is_accept_kwargs)
    True

    Ref: [1] https://github.com/flaggo/pydu/blob/master/pydu/inspect.py
    """
    return any([p for name, p in inspect.signature(func).parameters.items()
                if p.kind == p.POSITIONAL_OR_KEYWORD and name != 'self'])

def is_accept_varargs(func: Callable) -> bool:
    """Return True if the function `func` accepts `varargs` parameters, False otherwise.

    >>> is_accept_varargs(lambda *args: len(args) != 0)
    True
    >>> is_accept_varargs(lambda x: isinstance(x, (list, tuple, set)))
    False

    Ref: [1] https://github.com/flaggo/pydu/blob/master/pydu/inspect.py
    """
    return any(p for p in inspect.signature(func).parameters.values()
               if p.kind == p.VAR_POSITIONAL)

def is_accept_kwargs(func: Callable) -> bool:
    """Return True if the function `func` accepts `kwargs` parameters, False otherwise.

    >>> def add(a, b, **kwargs): ...
    >>> is_accept_kwargs(add)
    True
    >>> is_accept_kwargs(lambda x: x ** 2)
    False

    Ref: [1] https://github.com/flaggo/pydu/blob/master/pydu/inspect.py
    """
    return any(p for p in inspect.signature(func).parameters.values()
               if p.kind == p.VAR_KEYWORD)
