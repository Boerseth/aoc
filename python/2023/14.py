"""Parabolic Reflector Dish"""
from collections.abc import Iterator
from collections import defaultdict


TEST = """
O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....
""".strip()


CYCLE = NORTH, WEST, SOUTH, EAST = [1j ** i for i in range(1, 5)]


class Platform:
    def __init__(self, text: str) -> None:
        lines = text.strip().splitlines()
        self.ROWS = len(lines)
        self.COLS = len(lines[0])
        self.spaces = set()
        self.circles = set()
        for row, line in enumerate(reversed(lines)):
            for col, char in enumerate(line):
                pos = complex(col, row)
                if char != "#":
                    self.spaces.add(pos)
                if char == "O":
                    self.circles.add(pos)

    def tilt(self, direction: complex) -> None:
        high_first = direction in [NORTH, EAST]
        for circle in sorted(self.circles, key=lambda z: z.real + z.imag, reverse=high_first):
            self.circles.remove(circle)
            while (new := circle + direction) in self.spaces and new not in self.circles:
                circle = new
            self.circles.add(circle)

    def cycle(self) -> None:
        for direction in CYCLE:
            self.tilt(direction)

    def compute_load(self) -> int:
        return len(self.circles) + int(sum(self.circles).imag)

    def get_state(self) -> tuple[tuple[float, float], ...]:
        return tuple(sorted(int(c.real + self.ROWS * c.imag) for c in self.circles))

    def show(self) -> None:
        for row in reversed(range(self.ROWS)):
            for col in range(self.COLS):
                pos = complex(col, row)
                if pos in self.circles:
                    print("O", end="")
                    continue
                if pos in self.spaces:
                    print(".", end="")
                    continue
                print("#", end="")
            print()
        print()


def solve(text: str) -> Iterator:
    #text = TEST
    platform = Platform(text)
    platform.tilt(NORTH)
    yield platform.compute_load()

    platform = Platform(text)
    previous_states = {}
    loads = []
    counter = 0
    while platform.get_state() not in previous_states:
        loads.append(platform.compute_load())
        previous_states[platform.get_state()] = len(loads) - 1
        platform.cycle()
        counter += 1
    cycle_start = previous_states[platform.get_state()]
    cycle_end = len(loads)
    cycle = cycle_end - cycle_start
    equivalent_cycles = cycle_start + (1000000000 - cycle_start) % cycle
    print(cycle_start, cycle_end, cycle, equivalent_cycles)
    yield loads[equivalent_cycles]
