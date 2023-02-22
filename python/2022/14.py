"""Regolith Reservoir"""

from ast import literal_eval


SOURCE_LOCATION = 500
AIR = "."
ROCK = "#"
SAND = "o"
SOURCE = "+"


def parse_cave(text):
    paths = [[literal_eval(coord) for coord in line.split(" -> ")] for line in text.splitlines()]
    cave = {
        x + 1j * y: ROCK
        for path in paths
        for (x1, y1), (x2, y2) in zip(path, path[1:])
        for x in range(min(x1, x2), max(x1, x2) + 1)
        for y in range(min(y1, y2), max(y1, y2) + 1)
    }
    return cave | {SOURCE_LOCATION: SOURCE}


def open_spaces(z, cave, floor):
    for dx in [0, -1, 1]:
        z_next = z + 1j + dx
        if z_next not in cave and z_next.imag < floor:
            yield z_next


def flow(cave, sand_path, floor):
    if z_next := next(open_spaces(sand_path[-1], cave, floor), None):
        sand_path.append(z_next)
        return 0
    cave[sand_path.pop()] = SAND
    return 1


def solve(text):
    cave = parse_cave(text)
    sand_path = [SOURCE_LOCATION]
    y_max = max(key.imag for key in cave)

    # To be robust, should be a check on all sides for xmin, xmax, ymin, ymax
    grains_of_sand = 0
    while sand_path[-1].imag <= y_max:
        grains_of_sand += flow(cave, sand_path, y_max + 2)
    yield grains_of_sand

    while sand_path:
        grains_of_sand += flow(cave, sand_path, y_max + 2)
    yield grains_of_sand
