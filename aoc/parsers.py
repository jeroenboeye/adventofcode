"""Basic utility functions."""

from typing import (
    Any,
    Callable,
    List,
    Optional,
)

import numpy as np


def text_to_integer_array(text: str) -> np.ndarray:
    """Convert a string with newlines to a numpy array with integers."""
    return np.array([int(line) for line in text.splitlines()])


def unspaced_text_to_2d_list(text: str, dtype: Optional[Callable] = None) -> List[Any]:
    """
    Convert a string with newlines to a list with one element per character in the string.

    Optionally, dtype can be specified to convert the items elementwise.
    """
    if dtype is not None:
        return [[dtype(value) for value in line] for line in text.splitlines()]
    else:
        return [[value for value in line] for line in text.splitlines()]


def unspaced_text_to_2d_array(text: str, dtype: Optional[Callable] = None) -> np.ndarray:
    """Convert a string with newlines to a numpy array with one element per character in the string."""
    return np.array(unspaced_text_to_2d_list(text, dtype))
