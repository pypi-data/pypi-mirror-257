"""This module provides functionality for interacting with the machine.
"""

import os
import sys
import subprocess
from contextlib import contextmanager
from typing import Tuple, Dict

__all__ = [
    'is_windows',
    'is_linux',
    'is_posix',
    'is_darwin',
    'is_sunos',
    'is_smartos',
    'is_freebsd',
    'is_openbsd',
    'is_netbsd',
    'is_aix',
    'interpreter',
    'execute',
    'terminate',
    'environ',
    'change_dir',
    'is_on_ipython'
]

def is_windows() -> bool:
    """Return True if the current platform is Windows, False otherwise.

    Ref: [1] https://github.com/flaggo/pydu/blob/master/pydu/platform.py
    """
    return os.name == 'nt'

def is_linux() -> bool:
    """Return True if the current platform is Linux, False otherwise.

    Ref: [1] https://github.com/flaggo/pydu/blob/master/pydu/platform.py
    """
    return sys.platform.startswith('linux')

def is_posix() -> bool:
    """Return True if the current platform is POSIX, False otherwise.

    Ref: [1] https://github.com/flaggo/pydu/blob/master/pydu/platform.py
    """
    return os.name == 'posix'

def is_darwin() -> bool:
    """Return True if the current platform is Darwin, False otherwise.

    >>> is_darwin()
    True

    Ref: [1] https://github.com/flaggo/pydu/blob/master/pydu/platform.py
    """
    return sys.platform.startswith('darwin')

def is_sunos() -> bool:
    """Return True if the current platform is SunOS, False otherwise.

    Ref: [1] https://github.com/flaggo/pydu/blob/master/pydu/platform.py
    """
    return sys.platform.startswith('sunos')

def is_smartos() -> bool:
    """Return True if the current platform is SmartOS, False otherwise.

    Ref: [1] https://github.com/flaggo/pydu/blob/master/pydu/platform.py
    """
    return os.uname()[3].startswith('joyent_') if is_sunos() else False

def is_freebsd() -> bool:
    """Return True if the current platform is FreeBSD, False otherwise.

    Ref: [1] https://github.com/flaggo/pydu/blob/master/pydu/platform.py
    """
    return sys.platform.startswith('freebsd')

def is_netbsd() -> bool:
    """Return True if the current platform is NetBSD, False otherwise.

    Ref: [1] https://github.com/flaggo/pydu/blob/master/pydu/platform.py
    """
    return sys.platform.startswith('netbsd')

def is_openbsd() -> bool:
    """Return True if the current platform is OpenBSD, False otherwise.
    
    Ref: [1] https://github.com/flaggo/pydu/blob/master/pydu/platform.py
    """
    return sys.platform.startswith('openbsd')

def is_aix() -> bool:
    """Return True if the current platform is Aix, False otherwise.
    
    Ref: [1] https://github.com/flaggo/pydu/blob/master/pydu/platform.py
    """
    return sys.platform.startswith('aix')

def interpreter() -> str:
    """Return the Python interpreter path on the machine.

    >>> interpreter()
    '/Volumes/User/usr/lib/python/envs/pytorch_env/bin/python'
    """
    return sys.executable

def execute(command: str, shell: bool = False, env: dict = None, timeout: int = None) -> Tuple[int, str]:
    """Run cmd based on `subprocess.Popen` and return the tuple of `(return_code, stdout)`. Note that
    `stderr` is redirected to `stdout`.

    >>> execute('echo "hello world"', shell=True)
    (0, 'hello world\\n')

    Args:
        command (str): A command to be executed on a sub-process.
        shell (bool, optional): If true, the command will be executed through the shell.
        env (dict, optional): Defines the environment variables for the new process.
        timeout (int, optional): If the process does not terminate after `timeout` seconds,
            a `TimeoutExpired` exception will be raised.

    Ref: [1] https://github.com/flaggo/pydu/blob/master/pydu/cmd.py
    """
    p = subprocess.Popen(command, shell=shell, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=env)
    stdout, _ = p.communicate(timeout=timeout)
    return p.poll(), stdout.decode(sys.getdefaultencoding())

def terminate(pid: int) -> None:
    """Terminate process by given pid. On Windows, using Kernel32.TerminateProcess to kill.
    On Other platforms, using `os.kill` with `signal.SIGTERM` to kill.

    Ref: [1] https://github.com/flaggo/pydu/blob/master/pydu/cmd.py
    """
    if is_windows():
        import ctypes
        PROCESS_TERMINATE = 1
        handle = ctypes.windll.kernel32.OpenProcess(PROCESS_TERMINATE, False, pid)
        ctypes.windll.kernel32.TerminateProcess(handle, -1)
        ctypes.windll.kernel32.CloseHandle(handle)
    else:
        import signal
        os.kill(pid, signal.SIGTERM)

@contextmanager
def environ(**temp_env: Dict[str, str]) -> None:
    """Context manager for updating one or more environment variables. Preserves the previous environment
    variable (if available) and recovers when exiting the context manager. If given variable_name=None, it
    means removing the variable from environment temporarily.

    Ref: [1] https://github.com/flaggo/pydu/blob/master/pydu/environ.py
    """
    original_env = {}
    for key in temp_env:
        original_env[key] = os.environ.get(key, None)
        if temp_env[key] is not None:
            os.environ[key] = temp_env[key]
        elif original_env[key] is not None:
            del os.environ[key]
    yield None
    for key, value in original_env.items():
        if value is not None:
            os.environ[key] = value
        else:
            os.environ.pop(key, None)

@contextmanager
def change_dir(path: str) -> None:
    """Context manager for cd the given path.

    Ref: [1] https://github.com/flaggo/pydu/blob/master/pydu/path.py
    """
    old_path = os.getcwd()
    os.chdir(path)
    yield None
    os.chdir(old_path)

def is_on_ipython() -> bool:
    """Return whether the interpreter is on ipython.

    >>> is_on_ipython()
    False
    """
    return hasattr(__builtins__, '__IPYTHON__')
