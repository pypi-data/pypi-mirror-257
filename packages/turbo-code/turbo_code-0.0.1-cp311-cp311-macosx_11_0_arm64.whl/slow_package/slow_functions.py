"""
This is a module-level docstring
"""

import numpy as np
import numpy.typing as npt


def slow_add(a: int, b: int) -> int:
    """
    Add two numbers together.

    :param a: The first number to add.
    :type a: int
    :param b: The second number to add.
    :type b: int
    :return: The sum of `a` and `b`.
    :rtype: int
    """
    return a + b


def numpy_add(a: npt.NDArray, b: npt.NDArray) -> int:
    """
    Add two numpy arrays together.

    :param a: The first array to add.
    :type a: numpy.ndarray
    :param b: The second array to add.
    :type b: numpy.ndarray
    :return: The sum of `a` and `b`.
    :rtype: int
    """
    return np.add(a, b)
