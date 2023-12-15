"""Point of Incidence"""
from collections.abc import Iterator
from collections import defaultdict, Counter


def solve(text: str) -> Iterator[int]:
    patterns = [pattern.splitlines() for pattern in text.split("\n\n")]
    summary = defaultdict(int)
    for pattern in patterns:
        for multiplier, pat in [(100, pattern), (1, list(zip(*pattern)))]:
            for index in range(1, len(pat)):
                p1 = pat[index:]
                p2 = pat[:index][::-1]
                diff = sum(c1 != c2 for l1, l2 in zip(p1, p2) for c1, c2 in zip(l1, l2))
                summary[diff] += multiplier * index
    yield summary[0]
    yield summary[1]
