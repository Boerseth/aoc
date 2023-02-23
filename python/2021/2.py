"""Dive!"""

# Interpret movement as a complex number
# - Has direction and magnitude
# - Can be summed easily
def parse(command):
    if command.startswith("forward"):
        return int(command.split()[1])
    if command.startswith("down"):
        return int(command.split()[1]) * 1j
    if command.startswith("up"):
        return -int(command.split()[1]) * 1j
    raise Exception


def solve(text):
    steps = [parse(line) for line in text.splitlines()]
    aims = [sum(steps[: i + 1]).imag for i in range(len(steps))]
    yield (lambda z: int(z.real * z.imag))(sum(steps))

    answer = sum(z.real * (1 + 1j * aim) for z, aim in zip(steps, aims))
    yield int(answer.real * answer.imag)
