"""
Printing utilities.
"""

import inspect
from typing import (
    Any
)


def print_source_with_trimmed_doc(obj: Any) -> None:
    """
    
    """

    # is it a function?
    if inspect.isfunction(obj):

        # if, so is thiit a decorator?
        nonlocals = inspect.getclosurevars(obj).nonlocals

        # if so, print all enclosed functions
        # @TODO make it recursive
        if nonlocals:
            for field in nonlocals.values():
                if inspect.isfunction(field):
                    _print_source_with_trimmed_doc(field)
            return

    # if not a decorator or a function print the object source only
    _print_source_with_trimmed_doc(obj)


def _print_source_with_trimmed_doc(
        obj: Any
    ) -> None:
    """
    Prints the source lines of an object with only keeping
    the first line of the docstrings.

    Parameters:
        obj: Any : an object

    Returns:
        None : prints the source line to stdout
    """
    lines = inspect.getsourcelines(obj)[0]
    
    in_docstring = False
    add_to_buffer = False

    buffer = ["```python"]
    for line in lines:
        line = line.rstrip()

        token = line.strip()

        if (token == '"""') and not in_docstring:
            in_docstring = True
            add_to_buffer = True
        else:

            if in_docstring:
                if token == '"""':
                    in_docstring = False
                    add_to_buffer = False
                if token == "":
                    add_to_buffer = False

        if add_to_buffer:
            buffer.append(line)
        else:
            for lb in buffer:
                print(lb)
            buffer = []

        if not in_docstring:
            print(line)

    print("```")
