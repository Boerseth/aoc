"""Hot Springs"""
import re
from collections.abc import Iterator
from collections import defaultdict


def _get_positions(springs: str, group: int) -> list[tuple[int, int]]:
    pattern = f"(?<!#)(?=[?#]{{{group}}}(?!#))"
    positions = [(m.start(), m.start() + group) for m in re.finditer(pattern, springs)]
    return [(start, end, springs.rfind("#", 0, start)) for start, end in positions]


def _count_possibilities(springs: str, groups: list[int]) -> int:
    counts = {-1: 1}
    positions_lookup = {group: _get_positions(springs, group) for group in set(groups)}
    for group in groups:
        counts = {
            cend: sum(count for pend, count in counts.items() if pend >= cutoff and pend < cstart)
            for cstart, cend, cutoff in _get_positions(springs, group)
        }
    return sum(count for end, count in counts.items() if "#" not in springs[end:])


def get_positions(springs: str, group: int) -> list[tuple[int, int]]:
    pattern = f"(?<!#)(?=[?#]{{{group}}}(?!#))"
    return [(m.start(), m.start() + group) for m in re.finditer(pattern, springs)]


def count_possibilities(springs: str, groups: list[int]) -> int:
    counts = {(-1, -1): 1}
    positions_lookup = {group: get_positions(springs, group) for group in set(groups)}
    for group in groups:
        new_counts = defaultdict(int)
        for (prev_start, prev_end), count in sorted(counts.items()):
            next_disabled = springs.find("#", prev_end + 1) % (len(springs) + 1)
            for curr_start, curr_end in positions_lookup[group]:
                if curr_start <= prev_end:
                    continue
                if curr_start > next_disabled:
                    break
                new_counts[curr_start, curr_end] += count
        counts = new_counts
    return sum(count for (_, end), count in counts.items() if "#" not in springs[end:])


def solve(text: str) -> Iterator[int]:
    lines = [line.split() for line in text.strip().splitlines()]

    configs1 = [(arr, [int(g) for g in groups.split(",")]) for arr, groups in lines]
    yield sum(count_possibilities(arr, groups) for arr, groups in configs1)

    configs2 = [("?".join(arr for _ in "12345"), groups * 5) for arr, groups in configs1]
    yield sum(count_possibilities(arr, groups) for arr, groups in configs2)
