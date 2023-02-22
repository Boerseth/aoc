UP = "^"
DOWN = "v"
LEFT = "<"
RIGHT = ">"


def parse(text):
    top, *unstripped_rows, bottom = text.splitlines()
    assert top[:2] == "#." and all(c == "#" for c in top[2:])
    assert bottom[-2:] == ".#" and all(c == "#" for c in bottom[:-2])

    rows = [ur.strip("#") for ur in unstripped_rows]
    cols = list(zip(*rows))
    R = len(rows)
    C = len(cols)
    vertically_moving_blizzards = {
        direction: [{c for c, cell in enumerate(row) if cell == direction} for row in rows]
        for direction in [UP, DOWN]
    }
    horizontally_moving_blizzards = {
        direction: [{r for r, cell in enumerate(col) if cell == direction} for col in cols]
        for direction in [LEFT, RIGHT]
    }
    blizzards = vertically_moving_blizzards | horizontally_moving_blizzards
    return blizzards, R, C


def propagate_blizzards(blizzards, R, C):
    blizzards[UP].insert(R, blizzards[UP].pop(0))
    blizzards[DOWN].insert(0, blizzards[DOWN].pop())
    blizzards[LEFT].insert(C, blizzards[LEFT].pop(0))
    blizzards[RIGHT].insert(0, blizzards[RIGHT].pop())


def neighbourhood(R, C, r, c):
    yield r, c
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        if 0 <= r + dr < R and 0 <= c + dc < C:
            yield r + dr, c + dc


def explore(blizzards, open_spaces, R, C):
    propagate_blizzards(blizzards, R, C)
    open_spaces = {n for s in open_spaces for n in neighbourhood(R, C, *s)}
    open_spaces = {
        (r, c)
        for r, c in open_spaces
        if (r != R and c not in blizzards[UP][r])
        and (r != R and c not in blizzards[DOWN][r])
        and (c != C and r not in blizzards[LEFT][c])
        and (c != C and r not in blizzards[RIGHT][c])
    }
    return open_spaces


def count_minutes(blizzards, R, C, start, end):
    open_spaces = {start}
    steps = 0
    while not any(n in open_spaces for n in neighbourhood(R, C, *end)):
        open_spaces = explore(blizzards, open_spaces, R, C)
        steps += 1
    propagate_blizzards(blizzards, R, C),
    steps += 1
    return steps


def solve(text):
    blizzards, R, C = parse(text)
    START, END = (-1, 0), (R, C - 1)
    steps = 0
    steps += count_minutes(blizzards, R, C, START, END)
    yield steps
    steps += count_minutes(blizzards, R, C, END, START)
    steps += count_minutes(blizzards, R, C, START, END)
    yield steps


if __name__ == "__main__":
    from helpers import main_template

    main_template("24", solve)
