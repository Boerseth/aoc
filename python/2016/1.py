"""No Time for a Taxicab"""
from typing import Iterator


def parse(text: str) -> Iterator[str]:
    for word in text.strip().split(", "):
        turn = -1j if word[0] == "R" else 1j
        length = int(word[1:])
        yield turn, length


def part_1(instructions: list[tuple[complex, int]]) -> int:
    heading = complex(0, 1)
    position = complex(0, 0)
    for turn, length in instructions:
        heading *= turn
        position += length * heading
    return int(abs(position.real) + abs(position.imag))


def part_2(instructions: list[tuple[complex, int]]) -> int:
    visited = set()
    heading = complex(0, 1)
    position = complex(0, 0)
    for turn, length in instructions:
        heading *= turn
        for _ in range(length):
            position += heading
            if position in visited:
                return int(abs(position.real) + abs(position.imag))
            visited.add(position)


def solve(text: str) -> Iterator:
    instructions = list(parse(text))
    yield part_1(instructions)
    yield part_2(instructions)
