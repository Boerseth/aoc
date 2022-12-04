def solve():
    with open("inputs/4", "r") as f:
        lines = f.read().strip()
    id_pair_pairs = [
        eval(f'({line.replace(",", "),(").replace("-", ",")})')
        for line in lines.splitlines()
    ]
    # Pairs where one is fully inside the other
    yield sum(
        1
        for (min1, max1), (min2, max2) in id_pair_pairs
        if min1 <= min2 <= max2 <= max1 or min2 <= min1 <= max1 <= max2
    )
    # Pairs that overlap at all
    yield sum(
        1
        for (min1, max1), (min2, max2) in id_pair_pairs
        if not (max1 < min2 or max2 < min1)
    )


def solutions():
    yield 536
    yield 845


if __name__ == "__main__":
    from helpers import main_template

    main_template(solve, solutions)
