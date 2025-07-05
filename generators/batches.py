"""
Batch generator functions.
"""

from typing import (
    Any,
    Callable,
    Generator,
    Iterator
)


def serialiser(batches: Iterator) -> Generator:
    """
    Makes an elementwise generator from batches

    Parameters:
        batches: Iterator : batches!

    Returns:
        serialiser: Generator : generator of the individual
            elements in the batches
    """

    def serialise() -> Any:
        """
        Elementwise generator over batches.

        Parameters:
            None

        Yields:
            element: Any : element
        """

        for batch in batches:
            for element in batch:
                yield element

    return serialise()


def make_batcher(
        iterator: Iterator,
        n: int,
        strict: bool=True
    ) -> Generator:
    """
    Makes a generator of batches.

    Parameters:
        iterator: Iterator : iterator to be consumed
        n: int : size i.e. number of elements in batch
        strict: bool=True : whether to only allow batches
            batches of the specified size

    Returns:
        batcher: Generator : generator of batches
    """

    # will create a batch i.e. a generator of n elements when called call
    batch_function = _make_batch_function(iterator, n, strict)

    # yield batches from the iterator until it is exhausted
    batcher = loop_terminate_batch_function(batch_function)

    return batcher


def taker(
        iterator: Iterator,
        n: int,
        strict: bool
    ) -> Generator:
    """
    Makes a generator that takes a specified number of
    elements from an iterator.

    Parameters:
        iterator: Iterator : iterator to be consumed
        n: int : size i.e. number of elements in batch
        strict: bool=True : whether to only allow batches
            batches of the specified size

    Returns:
        taker: Generator : generator of a finite series of elements.
    """

    # create a taker function
    taken = _make_batch_function(iterator, n, strict)

    # return an instance of it
    return taken()


def _make_batch_function(
        iterator: Iterator,
        n: int,
        strict: bool
    ) -> Callable:
    """
    Makes a function that takes a specified number of
    elements from an iterator when called.

    Parameters:
        iterator: Iterator : iterator to be consumed
        n: int : size i.e. number of elements in batch
        strict: bool=True : whether to only allow batches
            batches of the specified size

    Returns:
        batch_function: Callable : generator of a finite series of elements.
    """

    def batch_function() -> Any:
        """
        Takes elements from an iterator and generates a batch of them.

        Parameters:
            None

        Yields:
            element : Any : an element in the batch.
        """

        i = 0
        while i < n:
            i += 1
            try:
                yield next(iterator)
            except StopIteration:
                break

        if n != 1 and strict:
            if (i != n) and (i != 1):
                raise ValueError()

    return batch_function


def loop_terminate_batch_function(
        batch_function: Callable
    ) -> Generator:
    """
    Creates batches and terminates them on an empty one.

    Parameters:
        batch_function: Callable : takes a batch of elements

    Yields:
        batch: Generator : a generator of batched elements
    """

    while True:
        batch = batch_function()

        try:
            element = next(batch)

            batch = prepend_generator(element, batch)
            yield batch

        except StopIteration:
            return


def prepend_generator(
        element_prepend: Any,
        generator: Generator
    ) -> Any:
    """
    Prepends an generator with an element.

    Parameters:
        element_prepend: Any : element to prepend
        generator: Generator : generator to augment

    Yields:
        : Any : first the prepended element
            then the elements of the generator
    """

    yield element_prepend
    for element in generator:
        yield element
