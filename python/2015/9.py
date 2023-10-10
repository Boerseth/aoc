"""All in a Single Night"""
from typing import Iterator


def generate_paths(locations, partial_path) -> Iterator[list[str]]:
    if len(locations) == len(partial_path):
        yield partial_path
        return
    for loc in sorted(locations - set(partial_path)):
        yield from generate_paths(locations, partial_path + [loc])


def solve(text: str) -> Iterator[int]:
    lengths = {}
    for line in text.splitlines():
        match line.split():
            case (start, "to", stop, "=", dist):
                lengths.setdefault(start, dict())[stop] = int(dist)
                lengths.setdefault(stop, dict())[start] = int(dist)

    locations = set(lengths)
    paths = generate_paths(locations, [])
    distances = [sum(lengths[a][b] for a, b in zip(path, path[1:])) for path in paths]

    yield min(distances)
    yield max(distances)
