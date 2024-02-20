""".. include:: ../../README.md"""
from typing import Union


def increment(x: Union[int, float]) -> Union[int, float]:
    """
    Add 1 to the given number.

    Parameters:
    x (int or float): Input number.

    Returns:
    int or float: Number x incremented by 1.
    """
    return x + 1
