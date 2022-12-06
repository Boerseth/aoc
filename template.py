def solve():
    N = 0
    with open(f"inputs/{N}", "r") as f:
        text = f.read()

    yield 0


def solutions():
    yield 0


if __name__ == "__main__":
    from helpers import main_template

    main_template(solve, solutions, with_assert=False)
