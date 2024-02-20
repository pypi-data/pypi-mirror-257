import pytest

from basket_case import fit_objects_into_baskets
from tests.fixtures import OBJECTS_4, OBJECTS_5, OVERSIZE_OBJECTS_1, OVERSIZE_OBJECTS_2, OVERSIZE_OBJECTS_ALL


def test_fit_no_objects():
    baskets = iter(fit_objects_into_baskets({}, 4))
    with pytest.raises(StopIteration):
        next(baskets)


@pytest.mark.parametrize(
    "objects,expected_oversize_objs",
    [
        (OVERSIZE_OBJECTS_ALL, OVERSIZE_OBJECTS_ALL),
        (OBJECTS_4|OVERSIZE_OBJECTS_1, OVERSIZE_OBJECTS_1),
        (OBJECTS_5|OVERSIZE_OBJECTS_2, OVERSIZE_OBJECTS_2),
    ],
    ids=[
        "all objects are oversize",
        "four objects with one oversize",
        "five objects with two oversize",
    ],
)
def test_fit_objects_bigger_than_basket_raises(objects, expected_oversize_objs):
    baskets = iter(fit_objects_into_baskets(objects, 4))
    try:
        next(baskets)
    except ValueError as err:
        assert err.args[0] == expected_oversize_objs
    assert objects


@pytest.mark.parametrize(
    "objects,basket_size,expected_baskets",
    [
        (OBJECTS_4, 3, [{'name0': 0, 'name1': 1, 'name2': 2}, {'name3': 3}]),
        (OBJECTS_5, 4, [{'name0': 0, 'name1': 1, 'name3': 3}, {'name4': 4}, {'name2': 2}]),
    ],
    ids=[
        "four objs, basket_size 3",
        "five objs, basket_size 4",
    ],
)
def test_fit_objects_no_oversize(objects, basket_size, expected_baskets):
    baskets = iter(fit_objects_into_baskets(objects, basket_size))
    for b, exp_b in zip(baskets, expected_baskets, strict=True):
        assert b == exp_b
    assert objects


@pytest.mark.parametrize(
    "objects,basket_size,expected_baskets",
    [
        (OBJECTS_4|OVERSIZE_OBJECTS_1, 3, [{'name0': 0, 'name3': 3}, {'name1': 1}]),
        (OBJECTS_5|OVERSIZE_OBJECTS_1, 4, [{'name0': 0, 'name1': 1, 'name3': 3}, {'name4': 4}]),
        (OBJECTS_5|OVERSIZE_OBJECTS_2, 4, [{'name0': 0, 'name4': 4}, {'name2': 2}]),
    ],
    ids=[
        "four objs with one oversize, basket_size 3",
        "five objs with one oversize, basket_size 4",
        "five objs with two oversize, basket_size 4",
    ],
)
def test_fit_objects_ignore_oversize(objects, basket_size, expected_baskets):
    baskets = iter(fit_objects_into_baskets(objects, basket_size, ignore_oversize=True))
    for b, exp_b in zip(baskets, expected_baskets, strict=True):
        assert b == exp_b
    assert objects


@pytest.mark.parametrize(
    "objects,basket_size,expected_baskets",
    [
        (OBJECTS_4|OVERSIZE_OBJECTS_1, 3, [{'name0': 0, 'name3': 3}, {'name1': 1}]),
        (OBJECTS_5|OVERSIZE_OBJECTS_1, 4, [{'name0': 0, 'name1': 1, 'name3': 3}, {'name4': 4}]),
        (OBJECTS_5|OVERSIZE_OBJECTS_2, 4, [{'name0': 0, 'name4': 4}, {'name2': 2}]),
    ],
    ids=[
        "four objs with one oversize, basket_size 3",
        "five objs with one oversize, basket_size 4",
        "five objs with two oversize, basket_size 4",
    ],
)
def test_fit_objects_corrupt_input_ignore_oversize(objects, basket_size, expected_baskets):
    baskets = iter(fit_objects_into_baskets(objects, basket_size, ignore_oversize=True, preserve_input=False))
    for b, exp_b in zip(baskets, expected_baskets, strict=True):
        assert b == exp_b
    assert not objects  # all consumed in-place
