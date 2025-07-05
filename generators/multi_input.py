"""
Multiple input generators.
"""

from typing import (
    Iterator,
    Generator,
    Tuple
)

from src.generators.batches import (
    loop_terminate_batch_function
)


def compressor(
        iterator: Iterator,
        selector: Iterator
    ) -> Generator:
    """
    Compressor generator. The an element of an iterator is yielded
    when the selector is true.

    Parameters:
        iterator: Iterator : elements to select
        selector: Iterator : selector

    Yields:
        element: Any : element
    """

    while True:
        try:
            element = next(iterator)
            if next(selector):
                yield element

        except StopIteration:
            return


def gater(
        iterator: Iterator,
        selector: Iterator
    ) -> Generator:
    """
    Gate generator. The next element of an iterator is yielded
    when the selector is true.

    Parameters:
        iterator: Iterator : elements to let pass or not
        selector: Iterator : gate

    Yields:
        : Any : element
    """

    while True:
        try:
            # only advance `iterator` if the condition is met
            # no elements are discarded
            if next(selector):
                yield next(iterator)

        except StopIteration:
            return


def merger(*iterators) -> Generator:
    """
    Merges (interlaces) iterators.

    Parameters:
        iterators: Any : list-like of iterators

    Yields:
        : Any : interlaced elements from the iterators
    """

    while True:
        for iterator in iterators:
            try:
                yield next(iterator)
            except StopIteration:
                return


def switcher(
        iterators: Tuple[Iterator],
        switch: Iterator
    ) -> Generator:
    """
    Selects elements from iterators based on the iterators' indices.

    Parameters:
        iterators: Tuple[Iterator] : iterators to choose elements from
        switch: Iterator : source of iterator indices 

    Yields:
        : Any : an element from the selected iterator
    """

    for which in switch:
        try:
            yield next(iterators[which])

        except StopIteration:
            return


def zipper(*iterators) -> Generator:
    """
    Collates elements from multiple iterators and yields the
    bundle as a single element.

    Parameters:
        iterators: Any : list-like of iterators

    Yields:
        : Tuple[Any]
    """

    def inner():
        for iterator in iterators:
            try:
                yield next(iterator)
            except StopIteration:
                return
    
    return loop_terminate_batch_function(inner)
