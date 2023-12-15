"""Lens Library"""
from collections.abc import Iterator


def holiday_ascii_string_helper(word: str) -> int:
    val = 0
    for char in word:
        val = ((val + ord(char)) * 17) % 256
    return val


class HashMap:
    def __init__(self) -> None:
        self.boxes = [[] for _ in range(256)]

    def remove(self, label: str) -> None:
        key = holiday_ascii_string_helper(label)
        self.boxes[key] = [
            (l, val) for l, val in self.boxes[key] if l != label
        ]

    def assign(self, label: str, value: str) -> None:
        key = holiday_ascii_string_helper(label)
        self.boxes[key] = [
            (l, val if l != label else value) for l, val in self.boxes[key]
        ]
        if label not in (l for l, _ in self.boxes[key]):
            self.boxes[key].append((label, value))

    def items(self) -> Iterator[tuple[int, int, str, str]]:
        for key, box in enumerate(self.boxes):
            for slot, (label, value) in enumerate(box):
                yield key, slot, label, value


def solve(text: str) -> Iterator:
    initialization_sequence = text.replace("\n", "").strip().split(",")

    verification_number = sum(map(holiday_ascii_string_helper, initialization_sequence))
    yield verification_number

    hashmap = HashMap()
    for step in initialization_sequence:
        if "-" in step:
            hashmap.remove(step.split("-")[0])
        if "=" in step:
            hashmap.assign(*step.split("="))
    focusing_power = sum((k + 1) * (s + 1) * int(v) for k, s, _, v in hashmap.items())
    yield focusing_power
