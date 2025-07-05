"""

"""

from typing import (
    Generator,
    Iterator,
    List,
    Tuple
)

import numpy as np

from src.generators.batches import (
    make_batcher,
    serialiser
)

from src.generators.multi_input import (
    switcher
)


def class_sampler(
        iterators: Tuple[Iterator],
        counts: Tuple[int]
    ) -> Generator:
    """
    Creates a generator of samples where each sample
    i) is a batch, ii) contains individuals from classes
    at a given number of times.

    Parameteres:
        generators: Tuple[Generator] : individuals by class
        counts: Tuple[int] : how many individual per class
            should be in a sample

    Returns:
        samples: Generator : sample generator
    """

    # first create a generator of class indices
    # each class appears the required number of times in each batch
    index_batches = generate_sample_index_batches(counts)

    # concatenate the batches so we can pass it to existing functions
    index_series = serialiser(index_batches)

    # contiguous samples
    gen_sample = switcher(iterators, index_series)

    # cut up to sample size batches
    samples = make_batcher(
        gen_sample, sum(counts), strict=False
    )

    return samples


def generate_sample_index_batches(
        counts: Tuple[int]
    ) -> Generator:
    """
    Generator of batch class indices.
    Each index appears at specified number
    of times in the sample and with equal probaibilty at any place.

    Parameters:
         counts: Tuple[int] : number of individiduals per class per sample

    Yields:
        : Generator : generator of batches of class indices 
    """

    while True:
        bookkeep = make_bookkeep(counts)
        yield sample_multiset_no_replacement(bookkeep)


def sample_multiset_no_replacement(bookkeep: Tuple[int]) -> Generator:
    """
    Generator of class indices in a sample.
    Each index appears at specified number
    of times in the sample and with equal probaibilty at any place.

    Parameters:
        bookkeep: List[int] : array to track class sample index ranges

    Yields:
        : int : class of the individual
    """

    n = len(bookkeep)

    # until all elements are taken
    while bookkeep[-1] != 0:

        # choose an element index
        i_pos = np.random.randint( bookkeep[-1])

        # find the class range in which it is found
        for i_class, i_pos_class_max in enumerate(bookkeep):
            if i_pos < i_pos_class_max:
                yield i_class - 1
                break

        # decrement the class index ranges by one
        # (shrink the mathced class and shift everything above)
        for i in range(i_class, n):
            # only if there are elements left in the class
            if bookkeep[i] == bookkeep[i - 1]:
                continue
            bookkeep[i] -= 1


def make_bookkeep(counts: Tuple[int]) -> List[int]:
    """
    Creates an array which is used to track how many
    individuals can be taken from each class in order to
    create a full sample.

    Parameters:
        counts: Tuple[int] : number of individiduals per class per sample

    Returns:
        bookkeep: List[int] : array to track class sample index ranges
    """

    bookkeep = [0]
    for i, count in enumerate(counts):
        bookkeep.append(bookkeep[- 1] + count)

    return bookkeep
