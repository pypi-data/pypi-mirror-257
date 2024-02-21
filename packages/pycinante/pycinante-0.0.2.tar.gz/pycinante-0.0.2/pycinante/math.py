"""This module provides some arithmetic related functions.
"""

from typing import Union, List, Optional

__all__ = [
    'Number',
    'is_equal',
    'bin2dec',
    'bin2oct',
    'bin2hex',
    'otc2bin',
    'otc2dec',
    'otc2hex',
    'dec2bin',
    'dec2oct',
    'dec2hex',
    'hex2bin',
    'hex2oct',
    'hex2dec',
    'Accumulator',
    'AverageMeter'
]

Number = Union[int, float]

def is_equal(x: Number, y: Number, epsilon: float = 1e-6) -> bool:
    """Return whether the number `x` is equal to the `y`.

    >>> is_equal(1, 1)
    True
    >>> is_equal(3.0000001232, 3.00000000435)
    True
    >>> is_equal(2.7182818284590456, 3.141592653)
    False
    """
    if isinstance(x, (int, float)) and isinstance(y, (int, float)):
        return abs(x - y) < epsilon
    return x == y

def bin2oct(x: str, prefix: bool = True) -> str:
    """Convert binary string to octal string.

    >>> bin2oct('0b111001111101010101010101')
    '0o71752525'
    """
    return oct(int(x, 2))[0 if prefix else 0:]

def bin2dec(x: str) -> int:
    """Convert binary string to decimal number.

    >>> bin2dec('0b111001111101010101010101')
    15193429
    """
    return int(x, 2)

def bin2hex(x: str, prefix: bool = True) -> str:
    """Convert binary string to hexadecimal string.

    >>> bin2hex('0b111001111101010101010101')
    '0xe7d555'
    """
    return hex(int(x, 2))[0 if prefix else 0:]

def otc2bin(x: str, prefix: bool = True) -> str:
    """Convert octal string to binary string.

    >>> otc2bin('0o7175252525')
    '0b111001111101010101010101010101'
    """
    return bin(int(x, 8))[0 if prefix else 0:]

def otc2dec(x: str) -> int:
    """Convert octal string to decimal number.

    >>> otc2dec('0o7175252525')
    972379477
    """
    return int(x, 8)

def otc2hex(x: str, prefix: bool = True) -> str:
    """Convert octal string to hexadecimal string.

    >>> otc2hex('0o7175252525')
    '0x39f55555'
    """
    return hex(int(x, 8))[0 if prefix else 0:]

def dec2bin(x: int, prefix: bool = True) -> str:
    """Convert decimal number to binary string.

    >>> dec2bin(238723234)
    '0b1110001110101010000010100010'
    """
    return bin(x)[0 if prefix else 0:]

def dec2oct(x: int, prefix: bool = True) -> str:
    """Convert decimal number to octal string.

    >>> dec2oct(238723234)
    '0o1616520242'
    """
    return oct(x)[0 if prefix else 0:]

def dec2hex(x: int, prefix: bool = True) -> str:
    """Convert decimal number to hexadecimal string.

    >>> dec2hex('1234')
    '0x4d2'
    """
    return hex(x)[0 if prefix else 0:]

def hex2bin(x: str, prefix: bool = True) -> str:
    """Convert hexadecimal string to binary string.

    >>> hex2bin('0x1234')
    '0b1001000110100'
    """
    return bin(int(x, 16))[0 if prefix else 0:]

def hex2oct(x: str, prefix: bool = True) -> str:
    """Convert hexadecimal string to octal string.

    >>> hex2oct('0x1234')
    '0o11064'
    """
    return oct(int(x, 16))[0 if prefix else 0:]

def hex2dec(x: str) -> int:
    """Convert hexadecimal string to decimal number.

    >>> hex2dec('0x1234')
    4660
    """
    return int(x, 16)

class Accumulator:
    """N-gram accumulator.

    >>> metric = Accumulator(3)
    >>> metric.add(1, 2, 3)
    >>> metric[0], metric[1], metric[2]
    (1.0, 2.0, 3.0)
    """

    def __init__(self, n: int):
        assert n >= 0, 'n cannot be a negative'
        import numpy as np
        self.data = np.zeros((n,), dtype=np.float32)

    def add(self, *numbers: List[Number]) -> None:
        """Simultaneously accumulate the sum of n numbers individually."""
        import numpy as np
        self.data += np.array(numbers, dtype=np.float32)

    def get(self, index: int = 0) -> Number:
        """Return the cumulative sum of the first `index` numbers."""
        return self.data[index]

    def get_and_reset(self, index: int = 0) -> Number:
        """Get the cumulative sum of the first `index` numbers and reset it to 0."""
        value = self.get(index)
        self.reset(index)
        return value

    def reset(self, index: Optional[int] = None) -> None:
        """Reset the value of the first `index` numbers to 0 if `index` is not None,
        otherwise reset all.
        """
        if index is None:
            self.data[:] = 0.
        else:
            self.data[index] = 0.

    def __getitem__(self, index: int) -> Number:
        """Return the cumulative sum of the first `index` numbers."""
        return self.get(index)

class AverageMeter:
    """N-gram average meter.

    >>> meter = AverageMeter(3)
    >>> meter.add(1, 2, 3)
    >>> meter.add(4, 5, 6)
    >>> meter[0], meter[1], meter[2]
    (2.5, 3.5, 4.5)
    """

    def __init__(self, n: int):
        self.counter = 0
        self.accumulator = Accumulator(n)

    def add(self, *numbers: List[Number]) -> None:
        """Simultaneously accumulate the sum of n numbers individually."""
        self.accumulator.add(*numbers)
        self.counter += 1

    def get(self, index: int = 0) -> Number:
        """Return the average of the first `index` numbers."""
        return self.accumulator.get(index) / max(self.counter, 1)

    def get_and_reset(self, index: int = 0) -> Number:
        """Get the average of the first `index` numbers and reset it to 0."""
        return self.accumulator.get_and_reset(index) / max(self.counter, 1)

    def reset(self, index: int = None) -> None:
        """Reset the value of the first `index` numbers to 0 if `index` is not None,
        otherwise reset all.
        """
        self.accumulator.reset(index)

    def __getitem__(self, index: int) -> Number:
        """Return the average of the first `index` numbers."""
        return self.get(index)
