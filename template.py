def solve(text):
    yield 0
    yield 0


if __name__ == "__main__":
    from helpers import main_template

    N = "0"
    main_template(N, solve, solutions=[0, 0], with_assert=False)
