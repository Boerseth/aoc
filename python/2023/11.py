"""Cosmic Expansion"""
from collections.abc import Iterable, Iterator
from itertools import combinations


def expand(pos: int, empties: Iterable[int], multiplier: int) -> int:
    return pos + (multiplier - 1) * sum(empty < pos for empty in empties)


def parse(text: str, multiplier: int = 2) -> None:
    lines = text.strip().splitlines()
    ROWS = len(lines)
    COLS = len(lines[0])

    galaxies = [
        (c, r) for r, line in enumerate(lines) for c, char in enumerate(line) if char == "#"
    ]
    empty_rows = set(range(ROWS)) - {r for _, r in galaxies}
    empty_cols = set(range(COLS)) - {c for c, _ in galaxies}
    new_cols = {c: expand(c, empty_cols, multiplier) for c in range(COLS)}
    new_rows = {r: expand(r, empty_rows, multiplier) for r in range(ROWS)}
    return [complex(new_cols[c], new_rows[r]) for c, r in galaxies]


def dist(z1: complex, z2: complex) -> float:
    d = z1 - z2
    return int(abs(d.imag) + abs(d.real))


def solve(text: str) -> Iterator:
    galaxies1 = parse(text, 2)
    yield sum(dist(g1, g2) for g1, g2 in combinations(galaxies1, 2))

    galaxies2 = parse(text, 1000000)
    yield sum(dist(g1, g2) for g1, g2 in combinations(galaxies2, 2))
