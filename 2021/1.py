def solve(text):
    depths = [int(line) for line in text.splitlines()]
    yield sum(1 for d1, d2 in zip(depths, depths[1:]) if d1 < d2)
    yield sum(1 for d1, d2 in zip(depths, depths[3:]) if d1 < d2)


if __name__ == "__main__":
    from helpers import main_template

    main_template("1", solve)
