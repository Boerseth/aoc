"""Let It Snow"""
from typing import Iterator


def get_code(row: int, col: int) -> int:
    code = 20151125
    for _ in range(1, col + ((row + col - 2) * (row + col - 1)) // 2):
        code = (252533 * code) % 33554393
    return code


def solve(text: str) -> Iterator[int | None]:
    words = text.replace(",", "").replace(".", "").split()
    row, col = [int(word) for word in words if word.isdigit()]
    yield get_code(row, col)
    yield None
