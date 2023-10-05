"""Probably a Fire Hazard"""
from enum import Enum
from typing import Iterator


class Command(str, Enum):
    ON = "on"
    OFF = "off"
    TOGGLE = "toggle"


Box = tuple[int, int, int, int]
Instruction = tuple[Command, Box]


def box_covers_other(this: Box, other: Box) -> bool:
    this_x1, this_x2, this_y1, this_y2 = this
    other_x1, other_x2, other_y1, other_y2 = other
    return (
        this_x1 <= other_x1 < other_x2 <= this_x2
        and this_y1 <= other_y1 < other_y2 <= this_y2
    )


def boxes_overlap(this: Box, other: Box) -> bool:
    this_x1, this_x2, this_y1, this_y2 = this
    other_x1, other_x2, other_y1, other_y2 = other
    if this_x2 <= other_x1 or other_x2 <= this_x1:
        return False
    if this_y2 <= other_y1 or other_y2 <= this_y1:
        return False
    return True


def partition(box: Box, other: Box) -> Iterator[Box]:
    if not boxes_overlap(box, other):
        yield box
        return
    x1, x2, y1, y2 = box
    x_vals = sorted({x1, x2, *[x for x in other[:2] if x1 < x < x2]})
    y_vals = sorted({y1, y2, *[y for y in other[2:] if y1 < y < y2]})
    for xx in zip(x_vals, x_vals[1:]):
        for yy in zip(y_vals, y_vals[1:]):
            yield (*xx, *yy)


def volume(box: Box) -> int:
    x1, x2, y1, y2 = box
    return (x2 - x1) * (y2 - y1)


def part_1(instructions: list) -> int:
    lights: set[Box] = set()
    for command, box in instructions:
        parts = {part for other_box in lights for part in partition(other_box, box)}
        inner = {part for part in parts if box_covers_other(box, part)}
        lights = parts - inner

        if command == Command.OFF:
            continue
        if command == Command.ON:
            lights.add(box)
            continue
        toggled_inner = [box]
        for inner_part in inner:
            toggled_inner = [
                part
                for toggled in toggled_inner
                for part in partition(toggled, inner_part)
                if not box_covers_other(inner_part, part)
            ]
        lights |= set(toggled_inner)
    return sum(map(volume, lights))


def get_new_brightness(bright: int, command: Command) -> int:
    if command == Command.OFF:
        return max(0, bright - 1)
    if command == Command.ON:
        return bright + 1
    if command == Command.TOGGLE:
        return bright + 2
    assert False


def part_2(instructions: list[Instruction]) -> int:
    brightness = {(0, 1000, 0, 1000): 0}
    for i, (command, box) in enumerate(instructions):
        brightness = {
            part: get_new_brightness(bright, command) if box_covers_other(box, part) else bright
            for other_box, bright in brightness.items()
            for part in partition(other_box, box)
        }
    return sum(bright * volume(box) for box, bright in brightness.items())


def new_parse(line) -> Instruction:
    *_, command, coords_1, _, coords_2 = line.split()
    x1, y1 = map(int, coords_1.split(","))
    x2, y2 = map(int, coords_2.split(","))
    assert command in list(Command)
    assert x1 <= x2 and y1 <= y2
    return Command(command), (x1, x2 + 1, y1, y2 + 1)


def solve(text: str) -> Iterator[int]:
    instructions = [new_parse(line) for line in text.strip().splitlines()]
    yield part_1(instructions)
    yield part_2(instructions)
