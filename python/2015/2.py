"""I Was Told There Would Be No Math"""


def solve(text):
    instructions = [sorted(map(int, line.split("x"))) for line in text.splitlines()]
    yield sum(3 * x * y + 2 * x * z + 2 * y * z for x, y, z in instructions)
    yield sum(2 * x + 2 * y + x * y * z for x, y, z in instructions)
