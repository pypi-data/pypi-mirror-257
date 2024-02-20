"""
Basket_case lib
"""

from collections import deque
import copy
from enum import Enum
import itertools as it
from typing import Iterator


class PredefinedSizes(Enum):
    """Helper values for common basket sizes
    """
    cd = 737280000
    dvd = 4707319808
    dvd_dl = 8543666176
    kb = 2**10
    mb = 2**20
    gb = 2**30
    tb = 2**40
    pb = 2**50


def fit_objects_into_baskets(
    objects: dict[str: int],
    basket_size: int,
    ignore_oversize: bool=False,
    preserve_input: bool=True,
) -> Iterator[dict[str, int]]:
    """Group the given objects into several baskets, maximising the room taken in each basket.

    Args:
        objects (dict[str: int]): each object expressed as name: size.
            Note: the size of an object can be zero (useful for files of zero length)
        basket_size (int): the size of the basket. All baskets have the same size.
        preserve_input (bool, optional): if True (default) do not corrupt the input (slower, more memory)
        ignore_oversize (bool, optional): if True ignore the oversize objects instead of raising ValueError

    Returns:
        Iterator[dict[str, int]]: each dict yielded represents a basket with its objects
            The number of resulting baskets depends on the cumulative size of the objects.

    Raises: 
        ValueError if any object is too big to fit in the basket. All such objects are made
             available in the exception's args attibute, as a dict.
             Can be suppressed with ignore_oversize=True
    """
    if not objects:
        return

    oversize_objects = {name: size for name, size in objects.items() if size>basket_size}
    if oversize_objects and not ignore_oversize:
        raise ValueError(oversize_objects)

    consume = deque(maxlen=0).extend
    if preserve_input:
        objects = copy.copy(objects)  # make a shallow copy of the input
    consume(objects.pop(name, None) for name in oversize_objects)  # remove the oversize objs
    while objects:
        best_comb_size = 0
        for k in range(1, len(objects)+1):
            for comb in it.combinations(objects, k):
                comb_size = sum(objects[name] for name in comb)
                if best_comb_size <= comb_size <= basket_size:
                    best_comb_size = comb_size  # update max size found
                    best_comb = comb  # save combination
        yield {name: objects[name] for name in best_comb}  # yield a basket
        consume(objects.pop(name, None) for name in best_comb)  # remove the objs in the comb
