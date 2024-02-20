# basket_case
A lib to fit objects of different size into multiple baskets (of the same size) optimally.

For example, use it to backup contents to CDs, DVDs, USB sticks, etc.

Note: the name refers to [a good horror film of the 80s](https://en.wikipedia.org/wiki/Basket_Case_(film))

## Repository

The lib code lives on gitlab at [this address](https://gitlab.com/pynchia/basket_case/)

## Notes

As it can be seen below, the time of computation grows exponentially based on the number of objects in input:

```
$ python tests/timings.py

Run with params:
    NUM_OBJECTS=28
    FREQ_OVERSIZE=6
    BASKET_SIZE=100
    NUM_TIMINGS=10
    
Preserving input: 50.43828155000028
Without preserving input: 5.0550676299999395

$ python tests/timings.py 
Run with params:
    NUM_OBJECTS=29
    FREQ_OVERSIZE=6
    BASKET_SIZE=100
    NUM_TIMINGS=10
    
Preserving input: 99.51453974099968
Without preserving input: 9.925193711000247
```
