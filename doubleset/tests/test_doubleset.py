from collections import defaultdict
from typing import DefaultDict

import pytest
from hypothesis import given, strategies as st

from doubleset import DoubleSet


@st.composite
def good_mapping(draw: st.DrawFn) -> DefaultDict[int, int]:
    mapping = draw(st.dictionaries(keys=st.integers(), values=st.integers()))
    return defaultdict(int, mapping)


@st.composite
def double_set(draw: st.DrawFn) -> DoubleSet:
    """
    hypothesis.strategies.composite is a way to create custom complex strategies.
    The `draw` function instantiates a strategy that is passed into it. The overall
    pattern for composite is

    ```python
    @st.composite
    def new_strategy(draw):
        generated_data = draw(some_preexisting_strategy())
        return apply_some_transformation(generated_data)
    ```

    `new_strategy` can then be used in future tests:

    ```python
    @given(x=new_strategy())
    def test_something(x):
        # ...
    ```
    """
    mapping = draw(good_mapping())
    return DoubleSet(mapping)


@given(x=double_set(), y=double_set())
def test_commutativity(x: DoubleSet, y: DoubleSet):
    assert x + y == y + x


@given(x=double_set(), y=double_set(), z=double_set())
def test_associativity(x: DoubleSet, y: DoubleSet, z: DoubleSet):
    assert (x + (y + z)) == ((x + y) + z)


@given(x=double_set())
def test_max_count_upon_instantiation_is_two(x):
    """The need for this test came up when test_membership was taking a really long time
    for seemingly no reason. After debugging, I realized that we weren't limiting counts
    to two when instantiating DoubleSet.
    """
    assert max([*x.counts.values(), 2]) == 2


@pytest.mark.timeout(30)  # in case count isn't being limited to 2
@given(x=good_mapping())
def test_membership(x: dict[int, int]):
    expected_members = {key for key in x if x[key] > 0}
    ds = DoubleSet(x)
    actual_members = {key for key in ds}
    assert expected_members == actual_members


def extract_counts(ds: DoubleSet) -> dict[int, int]:
    """Get a mapping of the number of occurrences of each element of ds"""
    counts: dict[int, int] = defaultdict(int)
    return counts


@given(x=double_set())
def test_max_count_is_two(x):
    counts: dict[int, int] = get_counts(x)

    if not counts:
        # If counts is empty, then this test should pass trivially, but
        # max([]) throws an error, so we need to have this guard clause
        return

    assert max(counts.values()) <= 2


@given(
    x=good_mapping(),
    y=good_mapping(),
)
def test_add(x: dict[int, int], y: dict[int, int]):
    expected_counts: dict[int, int] = {}
    add_to_and_update_target(target=expected_counts, source=x)
    add_to_and_update_target(target=expected_counts, source=y)

    x_ds = DoubleSet(x)
    y_ds = DoubleSet(y)
    z_ds: DoubleSet = x_ds + y_ds

    assert isinstance(z_ds, DoubleSet)

    actual_counts: dict[int, int] = get_counts(z_ds)

    assert expected_counts == actual_counts


def add_to_and_update_target(*, target: dict[int, int], source: dict[int, int]):
    for k, v in source.items():
        if v <= 0:
            # elements with nonpositive `count` shouldn't be included in
            continue

        # We decided to not use defaultdict for this because we'd need to convert
        # back to a dict to compare to the output of get_counts.
        # However, we still need to set a default value of 0 for the purposes
        # of this mock operation
        target[k] = target[k] if k in target else 0

        # Add the value from source
        target[k] += v

        # enforce max count of two
        target[k] = min((target[k], 2))

        # if the sum of all of the counts for key `k` is 0, that key shouldn't
        # be present in the DoubleSet
        if not target[k]:
            del target[k]


@pytest.mark.xfail()
def test_value_error():
    raise NotImplementedError


@pytest.mark.xfail()
def test_remove_element():
    raise NotImplementedError


@pytest.mark.xfail()
def test_remove_element_not_in_set():
    """Should raise an appropriate error when trying to delete an element from a set
    iff `raise==True`
    """
    raise NotImplementedError()


@pytest.mark.xfail()
def test_add_element():
    raise NotImplementedError


def get_counts(ds: DoubleSet) -> DefaultDict[int, int]:
    result: dict[int, int] = defaultdict(int)  # int() == 0
    for element in ds:
        result[element] += 1
    return result


@given(x=double_set(), y=double_set())
def test_subtract(x: DoubleSet, y: DoubleSet):

    expected_counts = get_counts(x)
    y_counts = get_counts(y)

    for element in expected_counts:
        expected_counts[element] -= y_counts[element]

    # Remove expected_counts
    expected_counts = {
        element: count for element, count in expected_counts.items() if count > 0
    }

    actual_counts = get_counts(x - y)

    assert expected_counts == actual_counts
