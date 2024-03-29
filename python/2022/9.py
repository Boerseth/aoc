"""Rope Bridge"""

from typing import Iterable


def get_tail_step(step: complex, head: complex, tail: complex) -> complex:
    diff = head + step - tail
    if abs(diff) < 2:
        return 0
    return (diff.real > 0) - (diff.real < 0) + 1j * ((diff.imag > 0) - (diff.imag < 0))


def get_steps(step: complex, knots: list[list[complex]]) -> list[complex]:
    steps = [step]
    for head, tail in zip(knots, knots[1:]):
        steps.append(get_tail_step(steps[-1], head, tail))
    return steps


def parse_input(text: str) -> Iterable[str]:
    for direction, length in map(str.split, text.splitlines()):
        step = {"R": 1, "L": -1, "U": 1j, "D": -1j}[direction]
        for _ in range(int(length)):
            yield step


def solve(text) -> Iterable[int]:
    N = 10
    ropes = [[0 for _ in range(N)]]
    for step in parse_input(text):
        steps = get_steps(step, ropes[-1])
        ropes.append([k + s for k, s in zip(ropes[-1], steps)])
    yield len(set(knots[1] for knots in ropes))
    yield len(set(knots[N - 1] for knots in ropes))
