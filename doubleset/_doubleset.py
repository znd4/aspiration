from __future__ import annotations

from collections import defaultdict
from typing import Iterator


class DoubleSet:
    def __init__(self, counts: dict[int, int] = None):
        self.counts = _initialize_counts(counts)

    def __add__(self, other) -> DoubleSet:
        counts = defaultdict(int)
        for element, count in self.counts.items():
            counts[element] += count

        for element, count in other.counts.items():
            counts[element] += count

        enforce_max_count(counts)

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
        >>> ds = DoubleSet({1: 2, 2: 1, 3: 0})
        >>> list(sorted(ds))
        [1, 1, 2]
        """
        for element, count in self.counts.items():
            # we should yield an element twice if there are two of it in self
            for _ in range(count):
                yield element


def enforce_max_count(counts: dict[int, int]) -> None:
    for element, count in counts.items():
        counts[element] = min((count, 2))


def _initialize_counts(counts: dict[int, int] | None = None):
    counts = counts or {}
    counts = {element: count for element, count in counts.items() if count}
    enforce_max_count(counts)
    counts = defaultdict(int, counts)
    return counts
