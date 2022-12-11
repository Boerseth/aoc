test_input = """addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop"""


def simulate(instructions):
    X = 1
    cycle = 0

    for instruction in instructions:
        cycle += 1
        yield X, cycle
        if instruction[0] == "addx":
            cycle += 1
            yield X, cycle
            X += int(instruction[1])


def solve(text):
    instructions = [line.split() for line in text.splitlines()]
    yield sum(X * cycle for X, cycle in simulate(instructions) if (cycle + 20) % 40 == 0)

    screen = [[" " for _ in range(40)] for _ in range(6)]
    for X, cycle in simulate(instructions):
        row = (cycle // 40) % 6
        pixel_pos = (cycle - 1) % 40
        if abs(X - pixel_pos) <= 1:
            screen[row][pixel_pos] = "#"
    yield "\n" + "\n".join("".join(line) for line in screen)


def solutions():
    yield 0
    yield 0


if __name__ == "__main__":
    with open(f"inputs/10", "r") as f:
        text = f.read()

    from helpers import main_template

    main_template(lambda: solve(text), solutions, with_assert=False)
