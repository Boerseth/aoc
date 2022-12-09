def get_tail_step(step: complex, head: complex, tail: complex):
    diff = head + step - tail
    if abs(diff) < 2:
        return 0
    return (diff.real > 0) - (diff.real < 0) + 1j * ((diff.imag > 0) - (diff.imag < 0))


def get_steps(step: complex, knots: list[list[complex]]):
    steps = [step]
    for head, tail in zip(knots, knots[1:]):
        steps.append(get_tail_step(steps[-1], head, tail))
    return steps


def parse_input(text):
    for direction, length in map(str.split, text.splitlines()):
        step = {"R": 1, "L": -1, "U": 1j, "D": -1j}[direction]
        for _ in range(int(length)):
            yield step


def solve():
    with open("inputs/9", "r") as f:
        text = f.read()
    N = 10
    ropes = [[0 for _ in range(N)]]
    for step in parse_input(text):
        steps = get_steps(step, ropes[-1])
        ropes.append([k + s for k, s in zip(ropes[-1], steps)])
    draw_rope_path(ropes)
    yield len(set(knots[1] for knots in ropes))
    yield len(set(knots[N - 1] for knots in ropes))


import matplotlib.pyplot as plt


colors = [
    "#FF0000",
    "#FF8000",
    "#FFFF00",

    "#80FF00",
    "#00FF00",
    "#00FF80",

    "#00FFFF",
    "#0080FF",
    "#0000FF",
    "#000000",
]
def draw_rope_path(ropes):
    paths = [([knots[i].real + i / 10 for knots in ropes], [knots[i].imag + i / 10 for knots in ropes]) for i in range(10)]
    fig = plt.figure(figsize=(20, 10))
    axes = plt.axes()
    axes.set_facecolor("white")
    axes.set_aspect("equal")
    for i, ((y, x), color) in enumerate(zip(paths, colors)):
        plt.plot(x, y, color=color, linewidth=0.3)
    plt.show()




def solutions():
    yield 6314
    yield 2504


if __name__ == "__main__":
    from helpers import main_template

    main_template(solve, solutions)
