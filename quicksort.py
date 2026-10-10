"""Deterministic and randomized in-place Quicksort implementations.

The deterministic algorithm chooses the last element as its pivot.
The randomized version chooses a uniformly random pivot within the current range.
Both use Lomuto partitioning and recursively process the smaller partition first,
limiting Python call-stack depth while retaining the standard partition behavior.
"""
from __future__ import annotations
import random
from typing import MutableSequence


def _partition(values: MutableSequence[int], low: int, high: int) -> int:
    """Partition around the value at high; return its final index."""
    pivot = values[high]
    i = low
    for j in range(low, high):
        if values[j] <= pivot:
            values[i], values[j] = values[j], values[i]
            i += 1
    values[i], values[high] = values[high], values[i]
    return i


def quicksort(values: MutableSequence[int]) -> MutableSequence[int]:
    """Sort values in place using a deterministic last-element pivot."""
    def sort(low: int, high: int) -> None:
        while low < high:
            pivot_index = _partition(values, low, high)
            if pivot_index - low < high - pivot_index:
                sort(low, pivot_index - 1)
                low = pivot_index + 1
            else:
                sort(pivot_index + 1, high)
                high = pivot_index - 1
    sort(0, len(values) - 1)
    return values


def randomized_quicksort(values: MutableSequence[int], rng: random.Random | None = None) -> MutableSequence[int]:
    """Sort values in place using randomly chosen pivots."""
    rng = rng if rng is not None else random.Random()
    def sort(low: int, high: int) -> None:
        while low < high:
            chosen = rng.randint(low, high)
            values[chosen], values[high] = values[high], values[chosen]
            pivot_index = _partition(values, low, high)
            if pivot_index - low < high - pivot_index:
                sort(low, pivot_index - 1)
                low = pivot_index + 1
            else:
                sort(pivot_index + 1, high)
                high = pivot_index - 1
    sort(0, len(values) - 1)
    return values


if __name__ == '__main__':
    example = [10, 7, 8, 9, 1, 5, 3]
    for function in (quicksort, randomized_quicksort):
        data = example.copy()
        function(data)
        print(f'{function.__name__}: {data}')
