"""Sonar Sweep"""


def solve(text):
    depths = [int(line) for line in text.splitlines()]
    yield sum(1 for d1, d2 in zip(depths, depths[1:]) if d1 < d2)
    yield sum(1 for d1, d2 in zip(depths, depths[3:]) if d1 < d2)
