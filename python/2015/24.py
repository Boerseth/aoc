"""It Hangs in the Balance"""
from typing import Iterator


def get_smallest_partitions(
    packages: list[int], goal: int, start: int = 0, smallest: int = None
) -> Iterator[list[int]]:
    smallest = len(packages) / 4 if smallest is None else smallest
    for index, package in enumerate(packages[start:], start):
        if package > goal:
            break
        if package == goal:
            yield [index]
            smallest = 1
            continue
        if smallest <= 1:
            break
        for sub_group in get_smallest_partitions(packages, goal - package, index + 1, smallest - 1):
            if smallest >= 1 + len(sub_group):
                smallest = 1 + len(sub_group)
                yield [index, *sub_group]


def product(factors: list[int]):
    p = 1
    for factor in factors:
        p *= factor
    return p


def get_smallest_partition_lowest_entanglement(packages, remaining, partitions: int) -> int:
    assert remaining[0] % partitions == 0
    partition_size = remaining[0] // partitions
    parts = {}
    for part in get_smallest_partitions(packages, partition_size):
        if len(part) not in parts:
            parts[len(part)] = []
        parts[len(part)].append(part)
    smallest_partitions = parts[min(parts)]
    entanglements = [product([packages[p] for p in part]) for part in smallest_partitions]
    return min(entanglements)


def solve(text: str) -> Iterator:
    packages = sorted([int(p) for p in text.strip().splitlines()])
    remaining = [sum(packages[i:]) for i in range(len(packages))]
    yield get_smallest_partition_lowest_entanglement(packages, remaining, 3)
    yield get_smallest_partition_lowest_entanglement(packages, remaining, 4)
