"""
Misc function helpers.
"""

from typing import (
    Any,
    Callable
)

def curry_2arg(func: Callable, arg: Any) -> Callable:
    """
    Enable a binary function to have its arguments passed in two calls.

    Parameters:
        func: Callable : binary function
        args: Any : the second argument of the function

    Returns:
        inner: Callable : function with its 1st argument only
    """

    def inner(x: Callable) -> Any:
        """
        Calls the function with its 1st argument passed explicitly.

        Parameters:
            x: Any : 1st function arguments

        Returns:
            : Any : function result
        """
        return func(x, arg)
    return inner
