"""This module provides functions to parse and convert time.
"""

import time
from typing import Callable, Tuple, Type, Union, Any
from validator import require_not_none

__all__ = [
    'Timer',
    'TimeUnit',
    'Duration'
]

class Timer(object):
    """A timer can time how long does calling take as a context manager or decorator.
    If assign ``print_func`` with ``sys.stdout.write``, ``logger.info`` and so on,
    timer will print the spent time.

    >>> timer = Timer()
    >>> timer(lambda: time.sleep(5))()
    >>> assert 5 - timer.elapsed < 1e-6

    Ref: [1] https://github.com/flaggo/pydu/blob/master/pydu/dt.py
    """

    def __init__(self, print_func: Callable = None):
        self.elapsed = None
        self.print_func = print_func

    def __enter__(self) -> None:
        self.start = time.time()

    def __exit__(self, *_) -> None:
        self.elapsed = time.time() - self.start
        if self.print_func:
            self.print_func(self.__str__())

    def __call__(self, func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            with self:
                return func(*args, **kwargs)
        return wrapper

    def __str__(self) -> str:
        return 'Spent time: {}s'.format(self.elapsed)

def init_time_unit(clazz: Type['TimeUnit']) -> Type['TimeUnit']:
    clazz.DAYS = clazz(0, (1, 24, 1440, 864e2, 864e5, 864e8, 864e11))
    clazz.HOURS = clazz(1, (1 / 24, 1, 60, 36e2, 36e5, 36e8, 36e11))
    clazz.MINUTES = clazz(2, (1 / 1440, 1 / 60, 1, 60, 6e4, 6e7, 6e10))
    clazz.SECONDS = clazz(3, (1 / 864e2, 1 / 36e2, 1 / 60, 1, 1e3, 1e6, 1e9))
    clazz.MICROSECONDS = clazz(4, (1 / 864e8, 1 / 36e5, 1 / 6e4, 1e-3, 1, 1e3, 1e6))
    clazz.MILLISECONDS = clazz(5, (1 / 864e11, 1 / 36e8, 1 / 6e7, 1e-6, 1e-3, 1, 1e3))
    clazz.NANOSECONDS = clazz(6, (1 / 864e11, 1 / 36e11, 1 / 6e10, 1e-9, 1e-6, 1e-3, 1))
    return clazz

@init_time_unit
class TimeUnit(object):
    """A TimeUnit represents time durations at a given unit of granularity and provides
    utility methods to convert across units, and to perform timing and delay operations
    in these units.

    >>> TimeUnit.DAYS.to_days(10)
    10
    >>> TimeUnit.HOURS.to_minutes(2)
    120

    Ref: [1] https://docs.oracle.com/en/java/javase/11/docs/api/java.base/java/util/concurrent/TimeUnit.html
    """

    # Time unit representing twenty-four hours.
    DAYS: 'TimeUnit' = ...

    # Time unit representing sixty minutes.
    HOURS: 'TimeUnit' = ...

    # Time unit representing sixty seconds.
    MINUTES: 'TimeUnit' = ...

    # Time unit representing one second.
    SECONDS: 'TimeUnit' = ...

    # Time unit representing one thousandth of a second.
    MILLISECONDS: 'TimeUnit' = ...

    # Time unit representing one thousandth of a millisecond.
    MICROSECONDS: 'TimeUnit' = ...

    # Time unit representing one thousandth of a microsecond.
    NANOSECONDS: 'TimeUnit' = ...

    def __init__(self, index: int, ratio: Tuple[float, ...]):
        self.index = index
        # days, hours, minutes, seconds, micros, millis, nanos
        self.ratio = ratio

    def convert(self, duration: Union[int, float], unit: 'TimeUnit' = None) -> float:
        """Converts the given time duration in the given unit to self unit."""
        return (unit or self).ratio[self.index] * duration

    def sleep(self, timeout: Union[int, float]) -> None:
        """Performs a `time.sleep` using this time unit."""
        time.sleep(self.to_seconds(timeout))

    def to_days(self, duration: Union[int, float]) -> float:
        """Equivalent to DAYS.convert(duration, self)."""
        return TimeUnit.DAYS.convert(duration, self)

    def to_hours(self, duration: Union[int, float]) -> float:
        """	Equivalent to HOURS.convert(duration, self)."""
        return TimeUnit.HOURS.convert(duration, self)

    def to_minutes(self, duration: Union[int, float]) -> float:
        """Equivalent to MINUTES.convert(duration, self)."""
        return TimeUnit.MINUTES.convert(duration, self)

    def to_seconds(self, duration: Union[int, float]) -> float:
        """Equivalent to SECONDS.convert(duration, self)."""
        return TimeUnit.SECONDS.convert(duration, self)

    def to_micros(self, duration: Union[int, float]) -> float:
        """Equivalent to MICROSECONDS.convert(duration, self)."""
        return TimeUnit.MICROSECONDS.convert(duration, self)

    def to_millis(self, duration: Union[int, float]) -> float:
        """Equivalent to MILLISECONDS.convert(duration, self)."""
        return TimeUnit.MILLISECONDS.convert(duration, self)

    def to_nanos(self, duration: Union[int, float]) -> float:
        """Equivalent to NANOSECONDS.convert(duration, self)."""
        return TimeUnit.NANOSECONDS.convert(duration, self)

class Duration(object):
    """A time-based amount of time, such as '34.5 seconds'. This class models a quantity or amount
    of time in terms of seconds and nanoseconds. It can be accessed using other duration-based units,
    such as minutes and hours.

    >>> Duration.of_hours(12).to_days()
    0.5

    Ref: [1] https://docs.oracle.com/en/java/javase/11/docs/api/java.base/java/time/Duration.html
    """

    def __init__(self, amount: Union[int, float], unit: TimeUnit):
        self.amount = amount
        self.unit = require_not_none(unit)

    def to_days(self) -> float:
        """Gets the number of days in this duration."""
        return self.unit.to_days(self.amount)

    def to_hours(self) -> float:
        """Gets the number of hours in this duration."""
        return self.unit.to_hours(self.amount)

    def to_minutes(self) -> float:
        """Gets the number of minutes in this duration."""
        return self.unit.to_minutes(self.amount)

    def to_seconds(self) -> float:
        """Gets the number of seconds in this duration."""
        return self.unit.to_seconds(self.amount)

    def to_millis(self) -> float:
        """Gets the number of milliseconds in this duration."""
        return self.unit.to_millis(self.amount)

    def to_micros(self) -> float:
        """Gets the number of microseconds in this duration."""
        return self.unit.to_micros(self.amount)

    def to_nanos(self) -> float:
        """Gets the number of nanoseconds in this duration."""
        return self.unit.to_nanos(self.amount)

    def plus(self, amount: Union[int, float], unit: TimeUnit) -> 'Duration':
        """Returns a copy of this duration with the specified duration added."""
        return Duration(self.amount + unit.convert(amount, self.unit), self.unit)

    def plus_days(self, days: Union[int, float]) -> 'Duration':
        """Returns a copy of this duration with the specified duration in standard 24-hour days added."""
        return self.plus(days, TimeUnit.DAYS)

    def plus_hours(self, hours: Union[int, float]) -> 'Duration':
        """Returns a copy of this duration with the specified duration in hours added."""
        return self.plus(hours, TimeUnit.HOURS)

    def plus_minutes(self, minutes: Union[int, float]) -> 'Duration':
        """Returns a copy of this duration with the specified duration in minutes added."""
        return self.plus(minutes, TimeUnit.MINUTES)

    def plus_seconds(self, seconds: Union[int, float]) -> 'Duration':
        """Returns a copy of this duration with the specified duration in seconds added."""
        return self.plus(seconds, TimeUnit.SECONDS)

    def plus_millis(self, milliseconds: Union[int, float]) -> 'Duration':
        """Returns a copy of this duration with the specified duration in milliseconds added."""
        return self.plus(milliseconds, TimeUnit.MILLISECONDS)

    def plus_nanos(self, nanoseconds: Union[int, float]) -> 'Duration':
        """Returns a copy of this duration with the specified duration in nanoseconds added."""
        return self.plus(nanoseconds, TimeUnit.NANOSECONDS)

    def minus(self, amount: Union[int, float], unit: TimeUnit) -> 'Duration':
        """Returns a copy of this duration with the specified duration subtracted."""
        return Duration(self.amount - unit.convert(amount, self.unit), self.unit)

    def minus_days(self, days: Union[int, float]) -> 'Duration':
        """Returns a copy of this duration with the specified duration in standard 24-hour days subtracted."""
        return self.minus(days, TimeUnit.DAYS)

    def minus_hours(self, hours: Union[int, float]) -> 'Duration':
        """Returns a copy of this duration with the specified duration in hours subtracted."""
        return self.minus(hours, TimeUnit.HOURS)

    def minus_minutes(self, minutes: Union[int, float]) -> 'Duration':
        """Returns a copy of this duration with the specified duration in minutes subtracted."""
        return self.minus(minutes, TimeUnit.MINUTES)

    def minus_seconds(self, seconds: Union[int, float]) -> 'Duration':
        """Returns a copy of this duration with the specified duration in seconds subtracted."""
        return self.minus(seconds, TimeUnit.SECONDS)

    def minus_millis(self, milliseconds: Union[int, float]) -> 'Duration':
        """Returns a copy of this duration with the specified duration in milliseconds subtracted."""
        return self.minus(milliseconds, TimeUnit.MILLISECONDS)

    def minus_nanos(self, nanoseconds: Union[int, float]) -> 'Duration':
        """Returns a copy of this duration with the specified duration in nanoseconds subtracted."""
        return self.minus(nanoseconds, TimeUnit.NANOSECONDS)

    def multiplied_by(self, amount: Union[int, float], unit: TimeUnit) -> 'Duration':
        """Returns a copy of this duration multiplied by the scalar."""
        return Duration(self.amount * unit.convert(amount, self.unit), self.unit)

    def divided_by(self, amount: Union[int, float], unit: TimeUnit) -> 'Duration':
        """Returns a copy of this duration divided by the specified value."""
        return Duration(self.amount / unit.convert(amount, self.unit), self.unit)

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Duration):
            return abs(self.amount - other.amount) < 1e-6
        return self.amount == other

    @staticmethod
    def of(amount: Union[int, float], unit: TimeUnit) -> 'Duration':
        """Obtains a Duration representing an amount in the specified unit."""
        return Duration(amount, unit)

    @staticmethod
    def of_days(days: Union[int, float]) -> 'Duration':
        """Obtains a Duration representing a number of standard 24-hour days."""
        return Duration(days, TimeUnit.DAYS)

    @staticmethod
    def of_hours(hours: Union[int, float]) -> 'Duration':
        """Obtains a Duration representing a number of standard hours."""
        return Duration(hours, TimeUnit.HOURS)

    @staticmethod
    def of_minutes(minutes: Union[int, float]) -> 'Duration':
        """Obtains a Duration representing a number of standard minutes."""
        return Duration(minutes * 60, TimeUnit.MINUTES)

    @staticmethod
    def of_seconds(seconds: Union[int, float]) -> 'Duration':
        """Obtains a Duration representing a number of seconds."""
        return Duration(seconds, TimeUnit.SECONDS)

    @staticmethod
    def of_millis(milliseconds: Union[int, float]) -> 'Duration':
        """Obtains a Duration representing a number of milliseconds."""
        return Duration(milliseconds, TimeUnit.MILLISECONDS)

    @staticmethod
    def of_micros(microseconds: Union[int, float]) -> 'Duration':
        """Obtains a Duration representing a number of microseconds."""
        return Duration(microseconds, TimeUnit.MICROSECONDS)

    @staticmethod
    def of_nanos(nanoseconds: Union[int, float]) -> 'Duration':
        """Obtains a Duration representing a number of nanoseconds."""
        return Duration(nanoseconds, TimeUnit.NANOSECONDS)
