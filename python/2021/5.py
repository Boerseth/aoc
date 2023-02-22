"""Hydrothermal Venture"""



def get_vent_locations_on_line(x1, y1, x2, y2):
    dx = int(x2 > x1) - int(x2 < x1)  # -1|0|1
    dy = int(y2 > y1) - int(y2 < y1)
    return [(x1 + n * dx, y1 + n * dy) for n in range(max(abs(x2 - x1), abs(y2 - y1)) + 1)]


def find_line_overlaps(vent_lines):
    vent_locations = set()
    overlaps = set()
    for line in vent_lines:
        for x, y in get_vent_locations_on_line(*line):
            if (x, y) in vent_locations:
                overlaps.add((x, y))
            else:
                vent_locations.add((x, y))
    return overlaps


def is_diagonal(x1, y1, x2, y2):
    return x1 != x2 and y1 != y2


def solve(text):
    lines = [
        [int(num) for xy in line.split(" -> ") for num in xy.split(",")]
        for line in text.splitlines()
    ]
    yield len(find_line_overlaps([l for l in lines if not is_diagonal(*l)]))
    yield len(find_line_overlaps(lines))
