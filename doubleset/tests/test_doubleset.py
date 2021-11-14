from collections import defaultdict
import pytest
from typing import DefaultDict
from doubleset import DoubleSet
from hypothesis import example, given, strategies as st, target


@st.composite
def good_mapping(draw: st.DrawFn) -> DefaultDict[int, int]:
    mapping = draw(st.dictionaries(keys=st.integers(), values=st.integers(min_value=0)))
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


@given(x=good_mapping())
def test_membership(x: dict[int, int]):
    expected_members = {key for key in x if x[key] != 0}
    ds = DoubleSet(x)
    actual_members = {key for key in ds}
    assert expected_members == actual_members


def extract_counts(ds: DoubleSet) -> dict[int, int]:
    """Get a mapping of the number of occurrences of each element of ds"""
    counts: dict[int, int] = defaultdict(int)
    return counts


@given(
    x=good_mapping(),
    y=good_mapping(),
)
def test_add(x: dict[int, int], y: dict[int, int]):
    x_ds = DoubleSet(x)
    y_ds = DoubleSet(y)


@pytest.mark.xfail()
def test_value_error():
    raise NotImplementedError


@pytest.mark.xfail()
def test_subtract():
    raise NotImplementedError
