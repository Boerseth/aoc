def solve():
    with open("inputs/6", "r") as f:
        text = f.read()
    # Find communicator message start position (len(unique) == 4) and stop (== 14)
    yield next(i for i in range(4, len(text)) if len(set(text[i - 4 : i])) == 4)
    yield next(i for i in range(14, len(text)) if len(set(text[i - 14 : i])) == 14)


def solutions():
    yield 1816
    yield 2625


if __name__ == "__main__":
    from helpers import main_template

    main_template(solve, solutions)
