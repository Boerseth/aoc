def priority(item: str) -> int:
    if item >= "a":
        return ord(item) + 1 - ord("a")
    return ord(item) + 27 - ord("A")


def sum_intersections(item_groups: list[list[str]]) -> int:
    overlaps = [set(g1).intersection(*map(set, gs)) for g1, *gs in item_groups]
    return sum(priority(item) for overlap in overlaps for item in overlap)


def solve() -> None:
    with open("inputs/3", "r") as f:
        rucksacks = f.read().strip().splitlines()

    yield sum_intersections((r[: len(r) // 2], r[len(r) // 2 :]) for r in rucksacks)
    yield sum_intersections(zip(*[rucksacks[i::3] for i in [0, 1, 2]]))


def solutions():
    yield 8394
    yield 2413


if __name__ == "__main__":
    from helpers import main_template

    main_template(solve, solutions)
