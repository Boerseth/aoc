"""Aunt Sue"""
from typing import Callable, Iterator


MFCSAM = """
children: 3
cats: 7
samoyeds: 2
pomeranians: 3
akitas: 0
vizslas: 0
goldfish: 5
trees: 3
cars: 2
perfumes: 1
""".strip().splitlines()
ANALYSIS = {k: int(v) for k, v in [line.split(": ") for line in MFCSAM]}


def parse_sue(raw: str) -> tuple[dict, int]:
    _, number, *rest = raw.strip().replace(":", "").replace(",", "").split()
    return number, {key: int(val) for key, val in zip(rest[::2], rest[1::2])}


def verify_1(key: str, val: int) -> bool:
    return val == ANALYSIS[key]


def verify_2(key: str, val: int) -> bool:
    if key in ["cats", "trees"]:
        return val > ANALYSIS[key]
    if key in ["pomeranians", "goldfish"]:
        return val < ANALYSIS[key]
    return val == ANALYSIS[key]


def find_sue(sues: list[tuple[int, dict]], verify: Callable) -> int | None:
    for number, sue in sues:
        if all(verify(key, val) for key, val in sue.items()):
            return number


def solve(text: str) -> Iterator[int | None]:
    sues = [parse_sue(line) for line in text.strip().splitlines()]
    yield find_sue(sues, verify_1)
    yield find_sue(sues, verify_2)
