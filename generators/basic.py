"""
Basic single input generators
"""

from typing import (
    Any,
    Callable,
    Iterator
)

def filtr(iterator: Iterator, cond: Callable) -> Any:
    """
    Makes a filtering generator. Only those elements yielded
    at which the condition evaluates to true.

   Parameters:
        iterator: Iterator : iterator!

    Yields:
        element: Any : a filtered element
    """

    for element in iterator:
        if cond(element):
            yield element


def identity(iterator: Iterator) -> Any:
    """
    Creates a generator that yields
    the elements of the consumed iterator

    Parameters:
        iterator: Iterator : iterator!

    Yields:
        element: Any : element from the base iterator
    """

    for element in iterator:
        yield element


def repeater(iterator: Iterator, n: int):
    """
    Creates a generator that repeats each element of the original
    iterator at specified times.

    Parameters:
        iterator: Iterator : iterator!
        n: int : how many times an element is yielded

    Returns:
        element: Any : repeated element
    """

    for element in iterator:
        for i in range(n):
            yield element



def thinner(iterator: Iterator, n: int) -> Any:
    """
    Creates a generator that selects every n-th element
    of the original iterator.

    Parameters:
        iterator: Iterator : iterator!
        n: int : n-th elements are yielded

    Yields:
        element: Any : n-th element
    """

    i = 0

    for el in iterator:
        if i % n == 0:
            yield el
        i += 1
