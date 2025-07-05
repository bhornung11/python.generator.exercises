"""
Generator multiplexer cf. itertools.tee
"""

import dataclasses

from typing import (
    Any,
    Dict,
    Generator,
    Iterator,
    Tuple
)

def multiplexer(
        iterator: Iterator,
        n: int
    ) -> Tuple[Generator]:
    """
    Creates indenpendent and identiacal generators from an iterator.

    Parameters:
        iterator: Iterator : iterator!
        n: int : number of generators to create

    Returns:
        multiplexed: Tuple[Generator] : effective copy of the
            original iterator as generators
    """

    teepot = TeePot(iterator, n)

    pot_manager = PotManager(teepot)

    multiplexed = tuple(
        TeeCup(i, pot_manager) for i in range(n)
    )

    return multiplexed


@dataclasses.dataclass
class TeePot:
    """
    Class to hold the shared resources and bookkeeping variables
    of multiplexed iterators.

    Attributes:
        iterator: Iterator : base source of elements
        n_gen: int : number of generators
        n_yielded: int : number of the yielded elements
        buffer: List[Any]: storage of the yielded elements
        generator_positions: Dict[int, int] : index of the last yielded
            element per generator
    """
    
    iterator: Iterator

    n_gen: int
    
    n_yielded: int = 0

    buffer: Dict[int, Any] = dataclasses.field(
        default_factory=dict
    )
    
    generator_positions: Dict[int, int] = dataclasses.field(
        default_factory=dict
    )

    def __post_init__(self) -> None:
        """
        Initialises the generator positions.
        """
        self.generator_positions = {
            i: - 1 for i in range(self.n_gen)
        }

class PotManager:
    """
    Class to retrieve elements from the shared resource of the
    multiplexed generator. Perform  bookkeeping.
    """

    def __init__(self, teepot: TeePot) -> None:
        """
        Add resource to the manager.

        Parameters:
            teepot: TeePot : shared resource of the multiplexed
                generators

        Returns:
            None
        """

        self.teepot = teepot
    
    def yield_next(self, idx: int, pos: int) -> Any:
        """
        Produces the next element from the selected generator.

        Parameters:
            idx: int : id of the generator
            pos: int : index of the element to be yielded

        Returns:
            element: Any : pos-th element of the idx-th generator
        """

        if pos > self.teepot.n_yielded:
            raise IndexError(
                "Iteration ahead of iterator. This should not happen..."
            )

        # take an element from the underlying iterator (1st access)
        if pos == self.teepot.n_yielded:
            
            element = next(self.teepot.iterator)

            self.teepot.buffer[pos] = element
            self.teepot.n_yielded += 1
            self.teepot.generator_positions[idx] = pos

            return element

        # take an element from the buffer (subsequent accesses)
        if pos < self.teepot.n_yielded:

            element = self.teepot.buffer[pos]

            self.teepot.generator_positions[idx] = pos
            self._trim_buffer(self.teepot)

            return element

    @staticmethod
    def _trim_buffer(teepot: TeePot) -> None:
        """
        Removes the elements from the shared resources which have
        already yielded by all generators.

        Parameters:
            teepot: TeePot : shared resource of the generators

        Returns:
            None
        """

        pos_min = min(teepot.generator_positions.values())
        positions_to_remove = [pos for pos in teepot.buffer if pos <= pos_min]

        for pos in positions_to_remove:
            del teepot.buffer[pos]
        
class TeeCup:
    """
    Class to mimic a generator which has copies.
    """

    def __init__(
            self,
            idx: int,
            pot_manager: PotManager
        ) -> None:
        """
        Multiplexed generator instance.

        Parameters:
            idx: int : generator id
            pot_manager: PotManager : shared resource manager

        Returns:
            None
        """
        self.idx = idx
        self.pos = 0
        self.pot_manager = pot_manager

    def __next__(self) -> Any:
        """
        Yields the subsequent element of a multiplexed generator.
        """

        element = self.pot_manager.yield_next(self.idx, self.pos)
        self.pos = self.pos + 1

        return element

    def __iter__(self):
        """Make an iterator. Sufficient to return self."""
        return self
