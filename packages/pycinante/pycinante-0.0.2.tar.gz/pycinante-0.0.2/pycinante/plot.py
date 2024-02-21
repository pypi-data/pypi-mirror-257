"""This module provides functions to plotting convincingly.
"""

from matplotlib import pyplot as plt
from matplotlib_inline import backend_inline
from typing import List, Union, Tuple
from pycinante.list import wrap
from pycinante.system import is_on_ipython
from pycinante.validator import check_condition

__all__ = [
    'Animator'
]

def set_axes(axes: plt.Axes, xlabel: str, ylabel: str, xlim: Union[int, Tuple[int, int]],
             ylim: Union[int, Tuple[int, int]], xscale: str, yscale: str, legend: List[str]) -> None:
    """Set the axes for matplotlib.

    Ref: [1] https://pypi.org/project/d2l/
    """
    axes.set_xlabel(xlabel), axes.set_ylabel(ylabel)
    axes.set_xscale(xscale), axes.set_yscale(yscale)
    axes.set_xlim(*wrap(xlim)), axes.set_ylim(*wrap(ylim))
    if legend:
        axes.legend(legend)
    axes.grid()

class Animator:
    """For plotting data in animation.

    Ref: [1] https://pypi.org/project/d2l/
    """

    @check_condition(is_on_ipython, 'A animator must be run in a notebook')
    def __init__(self, xlabel: str = None, ylabel: str = None, legend: List[str] = None,
                 xlim: Union[int, Tuple[int, int]] = None, ylim: Union[int, Tuple[int, int]] = None,
                 xscale: str = 'linear', yscale: str = 'linear', fmts: List[str] = ('-', 'm--', 'g-.', 'r:'),
                 nrows: int = 1, ncols: int = 1, figsize: Tuple[int, int] = (3.5, 2.5)):
        legend = legend or []
        backend_inline.set_matplotlib_formats('svg')
        self.fig, self.axes = plt.subplots(nrows, ncols, figsize=figsize)
        self.axes = (nrows * ncols == 1 and [self.axes, ]) or self.axes
        # Use a lambda function to capture arguments
        self.config_axes = lambda: set_axes(
            self.axes[0], xlabel, ylabel, xlim, ylim, xscale, yscale, legend)
        self.X, self.Y, self.fmts = None, None, fmts

    def add(self, x: Union[float, List[float]], y: Union[float, List[float]]) -> None:
        """Add multiple data points into the figure."""
        from IPython import display
        y = (not hasattr(y, '__len__') and [y]) or y
        n = len(y)
        x = (not hasattr(x, '__len__') and [x] * n) or x
        self.X = self.X or [[] for _ in range(n)]
        self.Y = self.Y or [[] for _ in range(n)]
        for i, (a, b) in enumerate(zip(x, y)):
            if a is not None and b is not None:
                self.X[i].append(a)
                self.Y[i].append(b)
        self.axes[0].cla()
        for x, y, fmt in zip(self.X, self.Y, self.fmts):
            self.axes[0].plot(x, y, fmt)
        self.config_axes()
        display.display(self.fig)
        display.clear_output(wait=True)
