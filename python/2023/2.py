"""Cube Conundrum"""
from collections.abc import Iterator
from dataclasses import dataclass


ZERO = {"red": 0, "green": 0, "blue": 0}


def parse_game(line: str) -> tuple[int, list[dict[str, int]]]:
    game_id_text, game_text = line.split(": ")
    game_id = int(game_id_text.split(" ")[1])

    subset_texts = game_text.split("; ")
    subsets = []
    for subs in subset_texts:
        color_text = [sub.split(" ") for sub in subs.split(", ")]
        subsets.append(ZERO | {color: int(value) for value, color in color_text})
    return game_id, subsets


def is_possible(subsets: list[dict[str, int]]) -> bool:
    return (
        max(s["red"] for s in subsets) <= 12
        and max(s["green"] for s in subsets) <= 13
        and max(s["blue"] for s in subsets) <= 14
    )


def power(subsets: list[dict[str, int]]) -> int:
    r, g, b = [max(s[key] for s in subsets) for key in ["red", "green", "blue"]]
    return r * g * b


def solve(text: str) -> Iterator:
    games = [parse_game(subsets) for subsets in text.strip().splitlines()]
    yield sum(game_id for game_id, subsets in games if is_possible(subsets))
    yield sum(power(subsets) for _, subsets in games)
