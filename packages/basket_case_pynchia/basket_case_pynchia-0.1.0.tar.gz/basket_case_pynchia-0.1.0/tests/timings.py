import random
import timeit

from basket_case import fit_objects_into_baskets

NUM_OBJECTS = 29
FREQ_OVERSIZE = 6  # i.e. one in six does not fit in the basket
BASKET_SIZE = 100
OBJECTS = {
    str(i): random.randrange(BASKET_SIZE+1) if i%FREQ_OVERSIZE else 99999999
    for i in range(NUM_OBJECTS)
}
NUM_TIMINGS = 10


print(
    f"""Run with params:
    {NUM_OBJECTS=}
    {FREQ_OVERSIZE=}
    {BASKET_SIZE=}
    {NUM_TIMINGS=}
    """
)

print("Preserving input:",
    timeit.timeit(
        lambda: list(
            fit_objects_into_baskets(
                OBJECTS,
                BASKET_SIZE,
                ignore_oversize=True,
                preserve_input=True,
            )
        ),
        number=NUM_TIMINGS
    )
)

print("Without preserving input:",
    timeit.timeit(
        lambda: list(
            fit_objects_into_baskets(
                OBJECTS,
                BASKET_SIZE,
                ignore_oversize=True,
                preserve_input=False
            )
        ),
        number=NUM_TIMINGS
    )
)
