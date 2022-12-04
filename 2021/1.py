def solve():
    depths = [int(line) for line in open("inputs/1", "r").readlines()]
    yield sum(1 for d1, d2 in zip(depths, depths[1:]) if d1 < d2)
    yield sum(1 for d1, d2 in zip(depths, depths[3:]) if d1 < d2)


def solutions():
    yield 1215
    yield 1150


if __name__ == "__main__":
    from helpers import main_template

    main_template(solve, solutions)
