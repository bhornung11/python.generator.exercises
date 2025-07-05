"""
Retrieve batches based on conditions.
"""

from typing import (
    Any,
    Callable,
    Generator,
    Iterator
)

from src.generators.batches import (
    loop_terminate_batch_function,
    prepend_generator
)


def make_batch_selector_cond1(
        iterator: Iterator,
        cond_start: Callable,
        yield_start: bool,
    ) -> Generator:
    """
    Creates a generator that splits the original stream to neighbouring
    batches. A batch starts when a condition is met.

    Parameters:
        iterator: Iterator : iterator!
        cond_start: Callable : condition to mark batcj start
        yield_start: bool : whether to yield element opening the batch

    Returns:
        selector: Generator : double conditional batch generator
    """
    # this is dirty => create a memory that is
    # persisted between batches
    _iterator = iter(iterator)

    def selector_func():
        """
        Generator function of batches starting at a condition.

        Parameters:
            None

        Yields:
            element: Any : element!
        """

        # share the memory with the inner function
        nonlocal _iterator
        
        has_batch_started = False

        for element in _iterator:

            if not has_batch_started:
                if cond_start(element):

                    if yield_start:
                        yield element

                    has_batch_started = True
            else:
                if cond_start(element):
                    # terminate iteration => a batch will be yielded
                    break
                else:
                    # select element to the batch
                    yield element

        # add back the sentinel element so that we can start a batch again
        _iterator = prepend_generator(element, _iterator)

    return loop_terminate_batch_function(selector_func)


def make_batch_selector_cond2(
        iterator: Iterator,
        cond_start: Callable,
        cond_end: Callable,
        yield_start: bool,
        yield_end: bool
    ) -> Generator:
    """
    Creates a generator of batches where a batch yields subsequent
    elements once a condition is satisfied until and other condition is met.

    Parameters:
        iterator: Iterator : iterator!
        cond_start: Callable : condition to mark batcj start
        cond_end: Callable : condition to mark batch end
        yield_start: bool : whether to yield element opening the batch
        yield_end: bool : whether to yield element closing the batch

    Returns:
        selector: Generator : double conditional batch generator
    """

    def selector_function() -> Any:
        """
        Generator function to produce elements between two conditions.

        Parameters:
            None

        Yields:
            element: Any : batch elements.
        """

        has_batch_started = False

        for element in iterator:

            if not has_batch_started:
                # start to select batch elements once the condition is met
                if cond_start(element):

                    if yield_start:
                        yield element
                    has_batch_started = True

            else:
                # end is signalled
                if cond_end(element):

                    if yield_end:
                        yield element

                    # terminate iteration so that the batch is yielded
                    break
                else:
                    # select more element to be the part of the batch
                    yield element

    selector = loop_terminate_batch_function(selector_function)

    return selector


def make_batch_selector_cond_count(
        iterator: Iterator,
        cond_start: Callable,
        n: int,
        yield_start: bool
    ) -> Generator:
    """
    Creates a generator that splits the original stream batches.
    A batch starts when a condition is met and ends when a given
    number of elements are yielded from it.

    Parameters:
        iterator: Iterator : iterator!
        cond_start: Callable : condition to mark batcj start
        n: int : number of elements in the batch
        yield_start: bool : whether to yield element opening the batch

    Returns:
        selector: Generator : double conditional batch generator
    """

    def selector_function() -> Any:
        """
        Condition and count batch generator function.

        Parameters:
            None

        Yields:
            element: Any : element!
        """

        has_batch_started = False
        # counter of elements selected to the batch
        i = 0

        for element in iterator:

            if not has_batch_started:
                if cond_start(element):

                    if yield_start:
                        i += 1
                        yield element

                    has_batch_started = True
            else:
                i += 1
                # enough elements in the batch =>
                if i == n + 1:
                    # => terminate iteration
                    break
                else:
                    # select element to the batch
                    yield element

    return loop_terminate_batch_function(selector_function)
