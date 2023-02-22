def solve():
    with open("inputs/2", "r") as f:
        text = f.read()
    instructions = [sorted(map(int, line.split("x"))) for line in text.splitlines()]
    yield sum(3 * x * y + 2 * x * z + 2 * y * z for x, y, z in instructions)
    yield sum(2 * x + 2 * y + x * y * z for x, y, z in instructions)


def solutions():
    yield 1586300
    yield 3737498


if __name__ == "__main__":
    from helpers import main_template

    main_template(solve, solutions)
