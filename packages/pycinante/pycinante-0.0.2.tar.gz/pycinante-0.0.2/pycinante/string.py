import locale
from typing import Any, Tuple, Union, List
from pycinante.reflect import cinvoke
from pycinante.list import wrap

__all__ = [
    'is_equal',
    'is_empty',
    'is_not_empty',
    'join',
    'get_default_encoding',
    'safe_encode',
    'lstrip',
    'rstrip',
    'strip',
    'longest_common_subsequence'
]

def is_equal(s: str, t: str, is_ignore_case: bool = False) -> bool:
    """Return True if s1 and s2 is equal, False otherwise.

    >>> is_equal('foo', 'bar')
    False
    >>> is_equal('Transformer Optimus Prime', 'transformer optimus prime')
    False
    >>> is_equal('Harry Potter', 'harry potter', True)
    True
    """
    return (cinvoke(is_ignore_case, s or '', 'lower') ==
            cinvoke(is_ignore_case, t or '', 'lower'))

def is_empty(s: str) -> bool:
    """Return True if the string is empty, False otherwise.

    >>> is_empty('')
    True
    >>> is_empty('   ')
    True
    >>> is_empty('Protoform')
    False
    """
    return s is None or len(s.strip()) == 0

def is_not_empty(s: str) -> bool:
    """Return True if the string is not empty, False otherwise.

    >>> is_not_empty('')
    False
    >>> is_not_empty('   ')
    False
    >>> is_not_empty('Scorponok')
    True
    """
    return s is not None and len(s.strip()) != 0

def join(*seq: Tuple[str], sep: str) -> str:
    """Concatenate any number of strings by the seperator `sep`.

    >>> join('Megatron', 'Starscream', 'Blackout', sep=', ')
    'Megatron, Starscream, Blackout'
    >>> join('Optimus Prime', 'Bumblebee', 'Ironhide', sep='/')
    'Optimus Prime/Bumblebee/Ironhide'
    """
    return sep.join(seq)

def get_default_encoding(encoding: str = None) -> str:
    """Return the charset that the user is likely using, according to the system configuration if
    the `encoding` is not specified.

    >>> get_default_encoding()
    'UTF-8'
    >>> get_default_encoding('GBK')
    'GBK'
    """
    return encoding or locale.getpreferredencoding()

def safe_encode(s: Any, encoding: str = 'utf-8') -> bytes:
    """Converts any given object to encoded string (default: utf-8).

    >>> safe_encode('hello')
    b'hello'
    >>> safe_encode('两年半')
    b'\xe4\xb8\xa4\xe5\xb9\xb4\xe5\x8d\x8a'
    >>> safe_encode([1, 2, 3])
    b'[1, 2, 3]'

    Ref: [1] https://github.com/flaggo/pydu/blob/master/pydu/string.py
    """
    if isinstance(s, str):
        return s.encode(encoding)
    if isinstance(s, bytes):
        return s
    return str(s).encode(encoding)

def lstrip(s: str, chars: Union[str, List[str]] = None) -> str:
    """Return a copy of the string with leading characters removed.

    >>> lstrip('abcdefghijklmnop', 'abc')
    'defghijklmnop'
    >>> lstrip('\t \t  abcdefghijklmnop', [' ', '\t'])
    'abcdefghijklmnop'

    Ref: [1] https://docs.python.org/3/library/stdtypes.html#str.lstrip
         [2] https://github.com/flaggo/pydu/blob/master/pydu/string.py
    """
    chars = wrap(chars or [' ', '\t', '\n'])
    while any([s.startswith(char) for char in chars]):
        for char in chars:
            s = (s.startswith(char) and s[len(char):]) or s
    return s

def rstrip(s: str, chars: Union[str, List[str]] = None) -> str:
    """Return a copy of the string with trailing characters removed.

    >>> rstrip('This is a sentence. \t \\n \t \\n')
    'This is a sentence.'

    Ref: [1] https://docs.python.org/3/library/stdtypes.html#str.rstrip
         [2] https://github.com/flaggo/pydu/blob/master/pydu/string.py
    """
    chars = wrap(chars or [' ', '\t', '\n'])
    while any([s.endswith(char) for char in chars]):
        for char in chars:
            s = (s.endswith(char) and s[:-len(char) or None]) or s
    return s

def strip(s: str, chars: Union[str, List[str]] = None) -> str:
    """Return a copy of the string with the leading and trailing characters removed.

    >>> strip('\\n  \\t \\n lists, tuples, sets   \\n  \\t')
    'lists, tuples, sets'

    Ref: [1] https://docs.python.org/3/library/stdtypes.html#str.strip
         [2] https://github.com/flaggo/pydu/blob/master/pydu/string.py
    """
    return rstrip(lstrip(s, chars), chars)

def longest_common_subsequence(s: str, t: str) -> str:
    """Return the longest common subsequence between `s` and `t`.

    >>> longest_common_subsequence('abcde', 'acdeb')
    'acde'
    """
    m, n = len(s), len(t)
    dp = [[0 for _ in range(n + 1)] for _ in range(m + 1)]
    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0 or j == 0:
                dp[i][j] = 0
            elif s[i - 1] == t[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    i, j, r = m, n, [''] * dp[m][n]
    while i > 0 and j > 0:
        if s[i - 1] == t[j - 1]:
            r[dp[m][n] - 1], i, j, dp[m][n] = s[i - 1], i - 1, j - 1, dp[m][n] - 1
        elif dp[i - 1][j] > dp[i][j - 1]:
            i = i - 1
        else:
            j = j - 1
    return ''.join(r)
