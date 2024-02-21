"""This module provides functionality for initializing an object.
"""

from typing import Dict, List, Union, Iterable

__all__ = [
    'NameFactory'
]

T = TypeVar('T')

class NameFactory(Dict[str, T]):
    """Naming Dict used to create an instance given its name.
    """

    def __init__(self, name: str, d: Union[Mapping[str, T], Iterable] = None):
        super(NameFactory, self).__init__(d or {})
        self.name = name

    @overload
    def build(self, name: List[str], *args: Tuple[Any], **kwargs: Dict[str, Any]) -> T:
        """Build an instance from the factory with the given instance name and return it."""
        pass

    @overload
    def build(self, names: Iterable[str], *args: Tuple[Any], **kwargs: Dict[str, Any]) -> List[T]:
        """Build a group of instances from the factory with the given instance name list and return it."""
        pass

    # noinspection PyRedeclaration
    def build(self, names: Union[str, Iterable[str]], *args: Tuple[Any], **kwargs: Dict[str, Any]) -> Union[T, List[T]]:
        """Build an instance or a group of instances from the factory with the given instance name.
        Note that if the type of names is an iterable, the keyword arguments should be {'name': kwargs, ...},
        if there is no keyword arguments, just nothing to provided in kwargs, e.g. {}. And the args
        will be passed all the constructor of the class when initializing the instance.

        Args:
            names (Union[str, Iterable[str]]): the class names to be initialized.
            *args (Tuple[Any]): the positional arguments to be passed to the constructor of the class.
            **kwargs (Dict[str, Any]): the keyword arguments to be passed to the constructor of the class.
        """
        if isinstance(names, str):
            if names not in self.keys():
                raise KeyError(f'Unknown name {names} for {self.name}')
            return self[names](*args, **kwargs)
        if isinstance(names, Iterable):
            instances = []
            for name in names:
                if name not in self.keys():
                    raise KeyError(f'Unknown name {name} for {self.name}')
                instances.append(self[name](*args, **kwargs.get(name, {})))
            return instances
        raise TypeError(f'Unsupported type {type(names)}')

    def __str__(self) -> str:
        return f'{self.name} ({super(NameFactory, self).__str__()})'
