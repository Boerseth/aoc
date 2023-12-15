"""Gear Ratios"""
from __future__ import annotations

from collections.abc import Iterator
from enum import Enum


class Type(str, Enum):
    BLANK = "blank"
    GEAR = "gear"
    NUMBER = "number"
    SYMBOL = "symbol"

    @staticmethod
    def from_char(char: str) -> Type:
        if char == ".":
            return Type.BLANK
        if char == "*":
            return Type.GEAR
        if char.isdigit():
            return Type.NUMBER
        return Type.SYMBOL


class Group:
    def __init__(self) -> None:
        self.type = None
        self.chars = []
        self.positions = []

    def add(self, char: str, position: complex) -> None:
        new_type = Type.from_char(char)
        assert self.type in [None, new_type]
        self.type = new_type
        self.positions.append(position)
        self.chars.append(char)

    def can_add(self, char: str, position: complex) -> None:
        if self.type is None:
            assert not self.chars and not self.positions
            return True
        new_type = Type.from_char(char)
        if self.type != new_type:
            return False
        if self.type == Type.SYMBOL:
            return False
        if (position - self.positions[-1]).real != 1:
            return False
        return True


def neighbours(z: complex) -> Iterator[complex]:
    for dz in [1, 1j, -1, -1j]:
        for rot in [1, 1 + 1j]:
            yield z + dz * rot


def parse(text: str) -> None:
    numbers = []
    position_to_index_map = {}

    groups = []
    for row, line in enumerate(text.strip().splitlines()):
        curr_group = Group()
        for col, char in enumerate(line):
            position = complex(col, row)
            if curr_group.can_add(char, position):
                curr_group.add(char, position)
            else:
                groups.append(curr_group)
                curr_group = Group()
                curr_group.add(char, position)
        groups.append(curr_group)

    return groups


def solve(text: str) -> Iterator[int]:
    groups = parse(text)

    symbols = set()
    for group in groups:
        if group.type in [Type.SYMBOL, Type.GEAR]:
            symbols.add(group.positions[0])

    numbers_base = {}
    numbers = {}
    for group in groups:
        if group.type != Type.NUMBER:
            continue
        base_pos = group.positions[0]
        for pos in group.positions:
            numbers_base[pos] = base_pos
        numbers[base_pos] = int("".join(group.chars))

    part_number_bases = set()
    for symbol in symbols:
        for neigh in neighbours(symbol):
            if neigh in numbers_base:
                part_number_bases.add(numbers_base[neigh])
    part_numbers = [numbers[base] for base in part_number_bases]
    yield sum(part_numbers)

    gears = set()
    for group in groups:
        if group.type == Type.GEAR:
            gears.add(group.positions[0])

    gear_ratios = []
    for gear in gears:
        base_neighs = {numbers_base[neigh] for neigh in neighbours(gear) if neigh in numbers_base}
        if len(base_neighs) == 2:
            factor1, factor2 = base_neighs
            gear_ratios.append(numbers[factor1] * numbers[factor2])

    yield sum(gear_ratios)
