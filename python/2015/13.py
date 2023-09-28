"""Knights of the Dinner Table"""
from typing import Iterator


def parse(text: str) -> dict[tuple[str, str], int]:
    graph = {}
    for line in text.splitlines():
        line = line[:-1] if line.endswith(".") else line
        pers1, _, feeling, units, *_, pers2 = line.split()
        change = int(units) * (1 if feeling == "gain" else -1)
        graph[pers1, pers2] = graph.setdefault((pers1, pers2), 0) + change
        graph[pers2, pers1] = graph.setdefault((pers2, pers1), 0) + change
    return graph


def get_permutations(items: set) -> Iterator[list]:
    if len(items) == 1:
        yield items
    else:
        for item in sorted(items):
            for permutation in get_permutations(items - {item}):
                yield [item, *permutation]


def compute_happiness(graph, order, with_me=False) -> int:
    return sum(
        graph[pers1, pers2]
        for pers1, pers2 in zip(order, order[1:] + ([] if with_me else [order[0]]))
    )


def solve(text: str) -> Iterator[int]:
    result = parse(text.strip())
    everyone = set(a for a, _ in result)
    yield max(compute_happiness(result, perm) for perm in get_permutations(everyone))
    yield max(compute_happiness(result, perm, True) for perm in get_permutations(everyone))
