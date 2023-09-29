"""No Such Thing as Too Much"""
from typing import Iterator


def get_combination_lengths(
    containers: list[int], remaining: list[int], goal: int, start: int = 0
) -> Iterator[int]:
    for i, container in enumerate(containers[start:], start):
        if container > goal:
            continue
        if container == goal:
            yield 1
            continue
        if remaining[i] < goal:
            break
        for length in get_combination_lengths(containers, remaining, goal - container, i + 1):
            yield 1 + length


def solve(text: str) -> Iterator[int]:
    containers = sorted([int(c) for c in text.strip().splitlines()], reverse=True)
    remaining = [sum(containers[i:]) for i in range(len(containers))]
    goal = 150

    combination_length_frequency = [0 for i in range(len(containers))]
    for combination_length in get_combination_lengths(containers, remaining, goal):
        combination_length_frequency[combination_length] += 1

    yield sum(combination_length_frequency)
    yield next(freq for freq in combination_length_frequency if freq)
