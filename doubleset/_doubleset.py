from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterator


class DoubleSet:
    """A modification of `set` that allows for up to two instances of each element.


    ```python linenums="1"
    from doubleset import DoubleSet
    ds = DoubleSet({0: 1, 1: 2})

    print(2 in ds)
    # False

    print(list(sorted(ds)))
    # [0, 1, 1]
    ```

    > note: `DoubleSet` only allows `int`s as values

    """

    def __init__(self, counts: dict[int, int] = None):
        self.counts: dict[int, int] = _initialize_counts(counts)

    def __add__(self, other) -> DoubleSet:
        counts = defaultdict(int)
        for element, count in self.counts.items():
            counts[element] += count

        for element, count in other.counts.items():
            counts[element] += count

        # max_count is enforced during DoubleSet creation. We used to also run
        # `enforce_max_count` here, but wew don't need to, so it's been removed
        # to remove a pointless O(N) scan
        return DoubleSet(counts)

    def __repr__(self):
        return f"DoubleSet({repr(self.counts)})"

    def __eq__(self, other) -> bool:
        if not hasattr(other, "counts"):
            raise ValueError("Cannot compare equality of DoubleSet and non-DoubleSet")
        return self.counts == other.counts

    def __iter__(self) -> Iterator[int]:
        """
        Rather than explicitly defining a __next__ method, or even creating a separate
        DoubleSetIterator class, I figured it would be better to stick with a generator.
        It's a nifty way to simplify the amount of code we need to write, and tbh it's
        clearer.
        This allows us to get

        ```python linenums="1"
        from doubleset import DoubleSet
        ds = DoubleSet({1: 2, 2: 1, 3: 0})
        list(sorted(ds))
        # [1, 1, 2]
        ```
        """
        for element, count in self.counts.items():
            # we should yield an element twice if there are two of it in self
            for _ in range(count):
                yield element

    def __sub__(self, other) -> DoubleSet:
        counts = defaultdict(int, self.counts)
        for element, count in other.counts.items():
            counts[element] -= count

        return DoubleSet(counts)


def remove_nonpositive_count_elements(counts: dict[int, int]) -> dict[int, int]:
    """(inplace) remove elemnts of `counts` with values <= 0"""
    return {element: count for element, count in counts.items() if count > 0}


def enforce_max_count(counts: dict[int, int]) -> dict[int, int]:
    return {element: min((count, 2)) for element, count in counts.items()}


def enforce_only_ints(counts: dict[int, int]):
    """Make sure that all of the elements and `count`s in `counts` are `int`s"""
    for element, count in counts.items():
        if not isinstance(element, int):
            raise ValueError(f"{element=}. All keys in counts should be ints.")

        if not isinstance(count, int):
            raise ValueError(f"{count=}. All values in counts should be ints.")


def _initialize_counts(counts: dict[int, int] | None = None):
    counts = counts or {}
    enforce_only_ints(counts)
    counts = remove_nonpositive_count_elements(counts)
    counts = enforce_max_count(counts)
    return counts
