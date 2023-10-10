"""Science for Hungry People"""
from dataclasses import dataclass
from typing import Iterator

import numpy as np


def parse(text: str) -> np.ndarray:
    return np.array(
        [
            [int(val) for val in line.split()[2::2]]
            for line in text.strip().replace(":", "").replace(",", "").splitlines()
        ]
    )


def compute_score(amounts: np.ndarray, ingredients: np.ndarray) -> int:
    return np.product(np.maximum(0, amounts @ ingredients))


def solve(text: str) -> Iterator[int]:
    # Great opportunity here for speed improvement with linear programming...
    # Just have to figure out what the inequalities are for each of the properties
    #   0  <  sum(amount[i] * ingredient[i].prop_j for all i)
    #         for all j
    data = parse(text)
    ingredients_1 = data[:, :4]
    calories = data[:, 4]
    max_score = 0
    max_score_2 = 0
    for f in range(101):
        for c in range(101 - f):
            for b in range(101 - f - c):
                s = 100 - f - c - b
                amounts = np.array([f, c, b, s])
                score = compute_score(amounts, ingredients_1)
                if score > max_score:
                    max_score = score
                if score > max_score_2 and amounts @ calories == 500:
                    max_score_2 = score
    yield max_score
    yield max_score_2
