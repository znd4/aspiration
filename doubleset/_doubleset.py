from __future__ import annotations

from collections import defaultdict


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


def enforce_max_count(counts: dict[int, int]) -> None:
    for element, count in counts.items():
        counts[element] = min((count, 2))


def _initialize_counts(counts: dict[int, int] | None = None):
    counts = counts or {}
    counts = {element: count for element, count in counts.items() if count}
    counts = defaultdict(int, counts)
    return counts
