"""This module provides functions to access and manipulate files.
"""

import glob
import os
import re
import shutil
import sys
import archive
from typing import *
from pycinante.list import wrap

__all__ = [
    'exists',
    'is_file',
    'is_dir',
    'mkdir',
    'drive',
    'parent',
    'basename',
    'filename',
    'extension',
    'ensure_extension',
    'extension_aware',
    'absolute_path',
    'canonical_path',
    'relative_path',
    'normalize_path',
    'sanitize_path',
    'join',
    'list_files',
    'copy',
    'move',
    'remove',
    'read',
    'write',
    'append',
    'clear',
    'PathBuilder',
    'load_pickle',
    'dump_pickle',
    'load_npy',
    'dump_npy',
    'load_pth',
    'dump_pth',
    'load_json',
    'dump_json',
    'load_yaml',
    'extract_archive'
]

def exists(pathname: str) -> bool:
    """Return True if path refers to an existing path or an open file descriptor.
    Returns False for broken symbolic links.

    >>> import tempfile
    >>> exists(tempfile.mktemp('.txt'))
    False
    >>> exists(tempfile.mkstemp('.txt')[1])
    True
    """
    return os.path.exists(pathname)

def is_file(pathname: str) -> bool:
    """Return True if path is an existing regular file.

    >>> import tempfile
    >>> is_file(tempfile.mkstemp('.txt')[1])
    True
    """
    return os.path.isfile(pathname)

def is_dir(pathname: str) -> bool:
    """Return True if path is an existing directory.

    >>> import tempfile
    >>> is_dir(tempfile.mkdtemp())
    True
    """
    return os.path.isdir(pathname)

def mkdir(pathname: str, parent: bool = False, **kwargs) -> None:
    """Create a directory. The argument `exist_ok` default is True.

    >>> mkdir('./a/b/c', parent=True)
    >>> assert not exists('./a/b/c')
    >>> shutil.rmtree('./a')
    """
    pathname = (parent and os.path.dirname(pathname)) or pathname
    os.makedirs(pathname, exist_ok=kwargs.pop('exist_ok', True), **kwargs)

def drive(pathname: str) -> str:
    """Return the drive of the pathname, where drive is either a mount point or the
    empty string.

    >>> drive('/usr/etc/bin/pycinante')
    ''
    """
    return os.path.splitdrive(pathname)[0]

def parent(pathname: str) -> str:
    """Return the parent directory of the file or directory `pathname`.

    >>> parent('/usr/etc/bin/pycinante')
    '/usr/etc/bin'
    """
    return os.path.dirname(pathname)

def basename(pathname: str) -> str:
    """Return the full name (included the extension) of the file on the `pathname`.

    >>> basename('/usr/etc/bin/pycinante.json')
    'pycinante.json'
    """
    return os.path.basename(pathname)

def filename(pathname: str) -> str:
    """Return the name (excluded the extension) of the file on the `pathname`.

    >>> filename('/usr/etc/bin/pycinante.json')
    'pycinante'
    """
    return os.path.basename(os.path.splitext(pathname)[0])

def extension(pathname: str) -> str:
    """Return the file extension of the file `pathname`.

    >>> extension('/usr/etc/bin/pycinante.json')
    '.json'
    """
    return os.path.splitext(pathname)[1]

def ensure_extension(pathname: str, ext: str) -> str:
    """Ensure that the pathname ends with the given extension.

    >>> ensure_extension('/usr/etc/bin/pycinante.json', '.json')
    '/usr/etc/bin/pycinante.json'
    >>> ensure_extension('/usr/etc/bin/pycinante', '.json')
    '/usr/etc/bin/pycinante.json'
    """
    ext = (ext.startswith('.') and ext) or ('.' + ext)
    pathname = (pathname.endswith('.') and pathname[:-1]) or pathname
    if not pathname.endswith(ext):
        pathname = pathname + ext
    return pathname

def extension_aware(pathname: str, ext: str) -> str:
    """Automatically append the given extension to the pathname if the pathname
    not a suffix.

    >>> extension_aware('/usr/etc/bin/pycinante.json', '.jsoup')
    '/usr/etc/bin/pycinante.json'
    >>> extension_aware('/usr/etc/bin/pycinante', '.json')
    '/usr/etc/bin/pycinante.json'
    """
    return (extension(pathname) and pathname) or ensure_extension(pathname, ext)

def absolute_path(pathname: str) -> str:
    """Return the absolute pathname of the file or directory `pathname`.

    >>> absolute_path('.')
    '/Volumes/User/home/chishengchen/Codespace/toy/pycinante/pycinante'
    """
    return os.path.abspath(pathname)

def canonical_path(pathname: str) -> str:
    """Return the canonical path of the specified filename, eliminating any symbolic
    links encountered in the path.

    >>> canonical_path('~/Codespace/toy/pycinante/./pycinante')
    '~/Codespace/toy/pycinante/pycinante'
    """
    return os.path.relpath(pathname)

def relative_path(pathname: str, start=None) -> str:
    """Return a relative filepath to path either from the current directory or from
    an optional start directory.

    >>> relative_path('/Volumes/User/home/chishengchen/Codespace/toy', '.')
    '../..'
    """
    return os.path.relpath(pathname, start=start or os.curdir)

def normalize_path(pathname: str) -> str:
    """Normalize a pathname by collapsing redundant separators.

    >>> normalize_path('~/Codespace/toy/./pycinante//.//pycinante')
    '~/Codespace/toy/pycinante/pycinante'
    """
    return os.path.normpath(pathname)

def sanitize_path(pathname: str, rep: str = None) -> str:
    """Replace all the invalid characters from a pathname with a char `rep`.

    >>> sanitize_path('A survey: Code is cheap, show me the code.pdf')
    'A survey Code is cheap, show me the code.pdf'
    """
    return re.sub(re.compile(r'[<>:"/\\|?*\x00-\x1F\x7F]'), rep or '', pathname)

def join(pathname: str, *pathnames: str) -> str:
    """Join one or more pathname segments intelligently. The return value is the
    concatenation of pathname and all members of *pathnames, with exactly one directory
    separator following each non-empty part, except the last.

    >>> join('/path/', 'etc', 'bin/', 'starting.conf')
    '/path/etc/bin/starting.conf'
    """
    return os.path.join(pathname, *pathnames)

def list_files(pathname: str, extensions: Union[str, List[str]] = None, **kwargs) -> List[str]:
    """Return a list of pathname matching a pathname pattern.

    >>> assert list_files('./', extensions=['.py'])
    """
    files = []
    for ext in wrap(extensions or ['*']):
        files.extend(glob.glob(os.path.join(pathname, f'*{ext}'), **kwargs))
    return files

def copy(src: str, dest: str) -> str:
    """Copy data and mode bits ("cp src dst"). Return the file's destination.

    >>> import tempfile
    >>> os.remove(copy(tempfile.mkstemp('.txt', text=True)[1], '.'))
    """
    return shutil.copy(src, dest)

def move(src: str, dest: str) -> str:
    """Recursively move a file or directory to another location. This is similar to the
    Unix "mv" command. Return the file or directory's destination.

    >>> import tempfile
    >>> os.remove(copy(tempfile.mkstemp('.txt', text=True)[1], '.'))
    """
    return shutil.move(src, dest)

def remove(pathname: str) -> None:
    """Recursively delete all files or folders in the pathname.

    >>> mkdir('./a/b/c/d/e/f/g')
    >>> remove('./a')
    >>> shutil.rmtree('./a')
    >>> assert os.system('touch tmp.txt') == 0
    >>> remove('tmp.txt')
    """
    if os.path.isdir(pathname):
        shutil.rmtree(pathname, ignore_errors=True)
        os.mkdir(pathname)
    else:
        os.remove(pathname)

def read(pathname: str, mode: str = 'r', **kwargs) -> AnyStr:
    """Read data from the file `pathname` and return it.

    >>> import tempfile
    >>> fd, filename = tempfile.mkstemp('.txt', text=True)
    >>> assert os.write(fd, b'hello world') == 11
    >>> read(filename, encoding='utf-8')
    'hello world'
    """
    with open(pathname, mode, **kwargs) as fp:
        return fp.read()

def write(data: AnyStr, pathname: str, mode: str = 'w', **kwargs) -> None:
    """Write the data to the file `pathname`.

    >>> import tempfile
    >>> filepath = tempfile.mktemp('.txt')
    >>> write('hello world', filepath)
    >>> read(filepath, encoding='utf-8')
    'hello world'
    """
    with open(pathname, mode, **kwargs) as fp:
        fp.write(data)

def append(data: Any, pathname: str, mode: str = 'a', **kwargs) -> None:
    """Append the data to the file `pathname`.

    >>> import tempfile
    >>> filepath = tempfile.mktemp('.txt')
    >>> write('hello world, ', filepath)
    >>> append('welcome to Pycinante!', filepath)
    >>> read(filepath, encoding='utf-8')
    'hello world, welcome to Pycinante!'
    """
    with open(pathname, mode, **kwargs) as fp:
        fp.write(data)

def clear(pathname: str) -> None:
    """Clear all the data on the file `pathname`.

    >>> import tempfile
    >>> filepath = tempfile.mktemp('.txt')
    >>> write('hello world, ', filepath)
    >>> clear(filepath)
    >>> read(filepath, encoding='utf-8')
    ''
    """
    with open(pathname, 'wb') as fp:
        fp.truncate()

class PathBuilder(object):
    """A pathname builder for easily constructing a pathname by the operation `/` and `+`.

    >>> p = PathBuilder('.', 'a', 'b', mkdir=False)
    >>> p / 'c' / 'd' / 'e' + 'f.json'
    './a/b/c/d/e/f.json'
    """

    def __init__(self, *pathname: Tuple[str, ...], mkdir: bool = True):
        self.path = os.path.join(*(pathname or ('.',)))
        self.mkdir = mkdir
        if self.mkdir:
            os.makedirs(self.path, exist_ok=True)

    def __truediv__(self, pathname: str) -> 'PathBuilder':
        """Append a sub-pathname to the original pathname and return a new pathname
        instance with the added sub-pathname.
        """
        return PathBuilder(os.path.join(self.path, pathname), mkdir=self.mkdir)

    def __add__(self, basename: str) -> str:
        """Append a basename to the original pathname and return the full pathname string
        after adding the basename.
        """
        return os.path.join(self.path, basename)

def load_pickle(pathname: str, **kwargs) -> Any:
    """Read a pickled object representation from the `.pkl` file.

    >>> dump_pickle({'name': 'Pycinante'}, 'test')
    >>> load_pickle('test')
    {'name': 'Pycinante'}
    >>> remove('test.pkl')
    """
    import pickle
    with open(extension_aware(pathname, '.pkl'), 'rb') as fp:
        return pickle.load(fp, **kwargs)

def dump_pickle(obj: Any, pathname: str, **kwargs) -> None:
    """Write a pickled representation of obj to the `.pkl` file.

    >>> dump_pickle({'name': 'Pycinante'}, 'test')
    >>> load_pickle('test')
    {'name': 'Pycinante'}
    >>> remove('test.pkl')
    """
    import pickle
    with open(extension_aware(pathname, '.pkl'), 'wb') as fp:
        pickle.dump(obj, fp, **kwargs)

# noinspection PyUnresolvedReferences
def load_npy(pathname: str, **kwargs) -> 'np.ndarray':
    """Load arrays or pickled objects from `.npz` or pickled files.

    >>> import numpy as np
    >>> dump_npy(np.array([7, 8, 9]), 'test')
    >>> load_npy('test')
    array([7, 8, 9])
    >>> remove('test.npy')
    """
    import numpy as np
    return np.load(extension_aware(pathname, '.npy'), **kwargs)

# noinspection PyUnresolvedReferences
def dump_npy(obj: 'np.ndarray', pathname: str, **kwargs) -> None:
    """Save an array to a binary file in NumPy ``.npz`` format.

    >>> import numpy as np
    >>> dump_npy(np.array([7, 8, 9]), 'test')
    >>> load_npy('test')
    array([7, 8, 9])
    >>> remove('test.npy')
    """
    import numpy as np
    np.save(extension_aware(pathname, '.npy'), obj, **kwargs)

# noinspection PyPackageRequirements
def load_pth(pathname: str, **kwargs) -> Any:
    """Loads an object saved with `torch.save` from a `.pth` file.

    >>> import torch
    >>> dump_pth(torch.tensor([7, 8, 9]), 'test')
    >>> load_pth('test')
    tensor([7, 8, 9])
    >>> remove('test.pth')
    """
    import torch
    return torch.load(extension_aware(pathname, '.pth'), **kwargs)

# noinspection PyPackageRequirements
def dump_pth(obj: Any, pathname: str, **kwargs) -> None:
    """Saves an object to a `.pth` disk file.

    >>> import torch
    >>> dump_pth(torch.tensor([7, 8, 9]), 'test')
    >>> load_pth('test')
    tensor([7, 8, 9])
    >>> remove('test.pth')
    """
    import torch
    torch.save(obj, extension_aware(pathname, '.pth'), **kwargs)

def load_json(pathname: str, encoding: str = None, **kwargs) -> Any:
    """Deserialize a file-like object containing a JSON document to a Python object.

    >>> dump_json({'name': 'Pycinante'}, 'test')
    >>> load_json('test')
    {'name': 'Pycinante'}
    >>> remove('test.json')
    """
    import json
    with open(extension_aware(pathname, '.json'), 'r', encoding=encoding or sys.getdefaultencoding()) as fp:
        return json.load(fp, **kwargs)

def dump_json(obj: Any, pathname: str, encoding: str = None, pretty: int = None, **kwargs) -> None:
    """Serialize the Python object `obj` into a json file.

    >>> dump_json({'name': 'Pycinante'}, 'test')
    >>> load_json('test')
    {'name': 'Pycinante'}
    >>> remove('test.json')
    """
    import json
    with open(extension_aware(pathname, '.json'), 'w', encoding=encoding or sys.getdefaultencoding()) as fp:
        json.dump(obj, fp, indent=kwargs.pop('indent', pretty), **kwargs)

# noinspection PyUnresolvedReferences,PyPackageRequirements
def load_yaml(pathname: str, loader: 'yaml.Loader' = None, encoding: str = None) -> dict:
    """Parse the YAML document in a file and produce the corresponding Python object."""
    import yaml
    with open(extension_aware(pathname, '.yml'), 'r', encoding=encoding or sys.getdefaultencoding()) as fp:
        return (loader or yaml.safe_load)(fp)

def extract_archive(src: str, dest: str) -> None:
    """Unpack the tar or zip file at the specified path to the directory specified by to_path.

    Ref: [1] https://flaggo.github.io/pydu/#/zh-cn/archive
         [2] https://pypi.org/project/python-archive/
    """
    assert extension(src).lower() in archive.extension_map.keys(), \
        f'unsupported compression format for the file {src}'
    archive.extract(src, dest)
