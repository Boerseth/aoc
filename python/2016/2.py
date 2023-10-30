"""Bathroom Security"""
from typing import Iterator


KEYPAD_1 = """
1 2 3
4 5 6
7 8 9
"""
KEYPAD_2 = """
    1
  2 3 4
5 6 7 8 9
  A B C
    D
"""
KEYPAD_1 = [l[0::2] for l in KEYPAD_1.splitlines() if l]
KEYPAD_2 = [l[0::2] for l in KEYPAD_2.splitlines() if l]


def get_neighbour_map(keypad: str):
    keys = set(c for line in keypad for c in line) - {' '}
    neighbour_map = {key: {d: key for d in "UDLR"} for key in keys}

    nei = {d: {key: key for key in keys} for d in "UDLR"}

    for line in keypad:
        for left, right in zip(line, line[1:]):
            if left in keys and right in keys:
                neighbour_map[left]["R"] = right
                neighbour_map[right]["L"] = left
    for line1, line2 in zip(keypad, keypad[1:]):
        for center, down in zip(line1, line2):
            if center in keys and down in keys:
                neighbour_map[center]["D"] = down
                neighbour_map[down]["U"] = center
    return neighbour_map


def find_next_button(
    button: int, instructions: str, neighbour_map: dict[str, dict[str, str]]
) -> str:
    for direction in instructions:
        button = neighbour_map[button][direction]
    return button


def find_digits(instructions: list[str], neighbour_map: dict[str, dict[str, str]]) -> str:
    button = "5"
    digits = ""
    for instruction in instructions:
        button = find_next_button(button, instruction, neighbour_map)
        digits += button
    return digits


def solve(text: str) -> Iterator:
    instructions = text.strip().splitlines()
    yield find_digits(instructions, get_neighbour_map(KEYPAD_1))
    yield find_digits(instructions, get_neighbour_map(KEYPAD_2))
