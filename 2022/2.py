def solve():
    matches = [line.strip().split() for line in open("inputs/2").readlines()]
    strategy = [(" ABC".find(s1), " XYZ".find(s2)) for s1, s2 in matches]
    points_1 = [
        shape_2 + ((1 + shape_2 - shape_1) % 3) * 3 for shape_1, shape_2 in strategy
    ]
    yield sum(points_1)
    points_2 = [
        1 + (shape_1 + outcome) % 3 + (outcome - 1) * 3 for shape_1, outcome in strategy
    ]
    yield sum(points_2)


def solutions():
    yield 13484
    yield 13433


if __name__ == "__main__":
    from helpers import main_template

    main_template(solve, solutions)
