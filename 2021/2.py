# Interpret movement as a complex number
# - Has direction and magnitude
# - Can be summed easily
def parse(command):
    if command.startswith("forward"): return int(command.split()[1])
    if command.startswith("down"): return int(command.split()[1]) * 1j
    if command.startswith("up"): return - int(command.split()[1]) * 1j
    raise Exception


def solve():
    steps = [parse(line) for line in open("inputs/2", "r").readlines()]
    aims = [sum(steps[: i + 1]).imag for i in range(len(steps))]
    yield (lambda z: int(z.real * z.imag))(sum(steps))

    answer = sum(z.real * (1 + 1j * aim) for z, aim in zip(steps, aims))
    yield int(answer.real * answer.imag)


def solutions():
    yield 1746616
    yield 1741971043


if __name__ == "__main__":
    from helpers import main_template

    main_template(solve, solutions)
