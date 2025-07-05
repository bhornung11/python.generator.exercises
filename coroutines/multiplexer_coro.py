
"""
Bare bones coroutine multiplexer.
"""

from typing import (
    Any,
    Callable,
    Generator,
    List
)

def start_coro(func: Callable) -> Callable:
    """
    Coroutine starter decorator.

    Parameters:
        func: Callable: coroutine

    Returns:
        starter: Callable : starter : coro starter
    """

    def starter(*args, **kwargs) -> Callable:
        """
        Coroutine starter.

        Parameters:
            *args : coro arguments
            **kwargs : coro keywords arguments

        Returns:
            started: Callable : started coroutine
        """

        started = func(*args, **kwargs)
        started.send(None)

        return started

    return starter

@start_coro
def multiplex_coro(targets: List[Callable]) -> Generator:
    """
    Sends an element to multiple coroutines.

    Parameters:
        targets: List[Callable] : list of target coros

    Returns:
        None: sends elements to targets
    """

    while True:
        element = (yield)
        for target in targets:
             target.send(element)

@start_coro
def filter_coro(cond: Callable, target: Callable) -> Generator:
    """
    Sends elements to a target which satisfy the specified condition.

    Parameters:
        cond: Callable : unary boolean function called on an element
        target: Callable : target

    Returns:
        None: sends selected elements to the target
    """

    # this loop is needed to keep the coroutine alive
    # otherwise it would exit after the first `send`
    while True:
        element = (yield)
        if cond(element):
            target.send(element)


@start_coro
def collector_coro(buffer: List[Any]) -> Generator:
    """
    Collects sent elements in a list.

    Parameters:
        buffer: List[Any]

    Returns:
        None : adds elements to buffer
    """

    while True:
        element = (yield)
        buffer.append(element)
