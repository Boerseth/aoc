"""Day 1: Trebuchet?!"""
from collections.abc import Iterable, Iterator


NAMES = ["", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
NUM_MAP = {str(num): num for num in range(1, 10)}
NAME_MAP = {NAMES[num]: num for num in range(1, 10)}


def extract_tokens(text: str, tokens: Iterable[str]) -> Iterator[str]:
    for i in range(len(text)):
        for token in tokens:
            if text[i:].startswith(token):
                yield token


def get_calibration_value(calibration: str, numeral_map: dict[str, int]) -> int:
    tokens = list(extract_tokens(calibration, numeral_map))
    first = numeral_map[tokens[0]]
    second = numeral_map[tokens[-1]]
    return 10 * first + second


def solve(text: str) -> Iterator[int]:
    lines = text.strip().splitlines()
    yield sum(get_calibration_value(line, NUM_MAP) for line in lines)
    yield sum(get_calibration_value(line, NUM_MAP | NAME_MAP) for line in lines)
