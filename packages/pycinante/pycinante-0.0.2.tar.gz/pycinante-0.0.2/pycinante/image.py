"""This module provides functions to access and manipulate images.
"""

try:
    from PIL import Image
    import numpy as np
except ImportError:
    pass

__all__ = [
    'opencv_loader',
    'pil_loader'
]

def opencv_loader(path: str) -> np.ndarray:
    """Load an image from the given path using the OpenCV."""
    import cv2
    return cv2.imread(path, cv2.COLOR_BGR2RGB)

def pil_loader(path: str) -> Image.Image:
    """Load an image from the given path using the PIL."""
    from PIL import Image
    return Image.open(path)
