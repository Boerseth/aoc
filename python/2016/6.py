"""Signals and Noise"""
from typing import Iterator


def get_counts(word: str) -> dict[str, int]:
    counts = {}
    for character in word:
        counts[character] = counts.get(character, 0) + 1
    return counts


def solve(text: str) -> Iterator[str]:
    rows = text.strip().splitlines()
    columns = [*zip(*rows)]
    all_counts = [get_counts(word) for word in columns]

    # most frequent letter every column
    yield "".join(max(counts, key=lambda c: counts[c]) for counts in all_counts)

    # least frequent letter every column
    yield "".join(min(counts, key=lambda c: counts[c]) for counts in all_counts)
