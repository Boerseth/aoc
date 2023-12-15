"""Pipe Maze"""
from collections.abc import Iterator


E, S, W, N = [1j ** n for n in range(4)]
INSIDE, OUTSIDE, BORDER = [-1, 1, 0]


PIPE_DIRECTIONS = {
    ".": [],
    "S": [E, S, W, N],
    "|": [N, S],
    "-": [W, E],
    "L": [N, E],
    "J": [N, W],
    "7": [S, W],
    "F": [S, E],
}
PIPES = {
    char: [(d1, d2) for d1 in dirs for d2 in set(dirs) - {d1}]
    for char, dirs in PIPE_DIRECTIONS.items()
}


def parse(text: str) -> dict[complex, str]:
    lines = text.strip().splitlines()
    return {complex(c, r): char for r, line in enumerate(lines) for c, char in enumerate(line)}


def get_start_and_maze(pipes: dict[complex, str]) -> tuple:
    pipe_groups = {char: [] for char in PIPES}
    for pos, char in pipes.items():
        pipe_groups[char].append(pos)
    [start] = pipe_groups["S"]
    maze = {
        pos: {pos + d1: pos + d2 for d1, d2 in PIPES[char]}
        for char, positions in pipe_groups.items()
        for pos in positions
    }
    maze[start] = {}
    return start, maze


def find_path(start: complex, maze: dict[complex, dict[complex, complex]]) -> list[complex]:
    direction = next(d for d in [N, E, S, W] if start in maze[start + d])
    path = [start, start + direction]
    while path[-1] != start:
        source, position = path[-2:]
        target = maze[position][source]
        path.append(target)
    return path


def has_region_changed(prev: str, curr: str) -> bool:
    if prev == "|":
        return True
    combined = f"{prev}{curr}"
    if combined in ["L7", "FJ"]:
        return True
    if combined in ["LJ", "F7"]:
        return False
    return False


def solve(text: str) -> Iterator:
    all_pipes = parse(text)
    start, maze = get_start_and_maze(all_pipes)
    path = find_path(start, maze)

    yield len(path) // 2

    first, last = path[1], path[-2]
    bend = {first - start, last - start}
    if bend == {1, -1}:
        all_pipes[start] = "-"
    if bend == {1j, -1j}:
        all_pipes[start] = "|"
    if bend == {1j, 1}:
        all_pipes[start] = "F"
    if bend == {1j, -1}:
        all_pipes[start] = "7"
    if bend == {-1j, 1}:
        all_pipes[start] = "L"
    if bend == {-1j, -1}:
        all_pipes[start] = "J"
    pipes = {pos: all_pipes[pos] for pos in path}

    INSIDE = True
    OUTSIDE = False

    count = 0
    MIN_ROW = 0
    MAX_ROW = 140
    rows = {r: [] for r in range(MIN_ROW, MAX_ROW + 1)}
    for p in path[1:]:
        rows[int(p.imag)].append(p)

    internal = []
    for r in range(MIN_ROW, MAX_ROW + 1):
        row = sorted(rows[r], key=lambda z: z.real)
        row = [p for p in row if pipes[p] != "-"]
        loop_index = 0
        for prev, curr in zip(row, row[1:]):
            if has_region_changed(pipes[prev], pipes[curr]):
                loop_index = (loop_index + 1) % 2
            if pipes[curr] in "|FL" and int(loop_index) % 2:
                count += int((curr - prev - 1).real)
                for ri in range(int(prev.real), int(curr.real) + 1):
                    internal.append(complex(ri, curr.imag))

    """
    path = set(path)
    internal = set(internal) - path
    for r in range(141):
        for c in range(141):
            pos = complex(c, r)
            if pos in internal:
                print("##", end="")
                continue
            if pos in path:
                print("+-", end="")
                continue
            print("  ", end="")
        print()
    """
    yield count
