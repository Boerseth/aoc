"""Squares With Three Sides"""
from typing import Iterator


def is_possible(triangle: tuple[int, int, int]) -> bool:
    return 2 * max(triangle) < sum(triangle)


def solve(text: str) -> Iterator:
    lines = [[int(i) for i in line.split()] for line in text.strip().splitlines()]
    yield sum(is_possible(triangle) for triangle in lines)

    triangles = [
        triangle
        for columns in zip(lines[::3], lines[1::3], lines[2::3])
        for triangle in zip(*columns)
    ]
    yield sum(is_possible(triangle) for triangle in triangles)
