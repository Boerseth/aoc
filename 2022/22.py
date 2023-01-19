INITIAL_DIRECTION = 1  # rightward


"""
# Description:
Each point on the field/cube has a position in the input, which gets encoded in
a complex number `z`. Directions ^ > v < can be represented by `1j ** n`.


# Goal:
Create a map `neighbours`:

    neighbours = {
        (point, direction): (neighbour_in_direction, direction_back_to_point)
    }
    neighbours[point, direction] = (neighbour_in_direction, direction_back_to_point)

    iff  neighbours[x] == y
    then neighbours[y] == x

And use it to traverse the field/cube from the instructions in the input.


# Part 1:
Building `neighbours` is fairly straightforward, and code is I would say clear.


# Part 2:
Each face of the cube corresponds to some square of symbols in the input. The
size of the squares `N` can be found (`get_size`), from which the points can be
split up into two parts:

    referance_frame(point, N) -> (origin, offset):
    - origin: Coordinates to the (0, 0) corner of a cube-face in the input.
    - offset: Coordinates of a point on a cube-face, relative to `origin`
    - point == origin + offset

Before returning, the `neighbours` map has a different definition:

    {
        (origin, offset): {
            direction: (neighbour_origin, neighbour_offset, direction_back)
        }
    }
    neighbours[origin, offset][direction] = (n_origin, n_offset, direction_back)

    iff  neighbours[x][sx] == (*y, sy)
    then neighbours[y][sy] == (*x, sx)

We can start by populating this `neighbours` map almost like in Part-1, except
we skip adding neighbours that fall outside the edge. Here, we also keep track
of any corner locations.

The next step is to stitch together the edges.
    - Find a corner point with its two neighbouring corner-points populated
    - If the two corners don't know about each other, populate `neighbours`
      along the corresponding edge.

Finally, compute the final `neighbours` map in coordinates corresponding to the
2D input and return.
"""


def get_size(spaces):
    N = int((len(spaces) // 6) ** 0.5)
    assert 6 * N ** 2 == len(spaces)
    return N


def referance_frame(position, size):
    origin = complex(int(position.real) // size, int(position.imag) // size) * size
    offset = complex(int(position.real) % size, int(position.imag) % size)
    return origin, offset


def get_neighbour_map_2(spaces):
    N = get_size(spaces)
    M = N - 1
    corner_neighbour_directions = {
        complex(0, 0): (-1j, -1),
        complex(M, 0): (1, -1j),
        complex(M, M): (1j, 1),
        complex(0, M): (-1, 1j),
    }

    corners = []
    neighbours = {}
    for position in spaces:
        origin, offset = referance_frame(position, N)
        neighbours[origin, offset] = {}
        for step in [1, -1, 1j, -1j]:
            neigh_position = position + step
            if neigh_position not in spaces:
                # On the edge; stitch together later
                continue
            neigh_origin, neigh_offset = referance_frame(neigh_position, N)
            neighbours[origin, offset][step] = (neigh_origin, neigh_offset, -step)
        if offset in corner_neighbour_directions:
            corners.append((origin, offset))

    # Stitch together edges
    while any(len(neighbours[point_on_cube]) != 4 for point_on_cube in corners):
        for origin, corner in corners:
            neighs = neighbours[origin, corner]
            # Looking for a corner neighbouring two other corners,
            # but the two other corners don't know about eachother yet.
            if len(neighs) != 4:
                continue
            step_to_left, step_to_right = corner_neighbour_directions[corner]
            origin_left, corner_left, step_from_left = neighs[step_to_left]
            origin_right, corner_right, step_from_right = neighs[step_to_right]
            if len(neighbours[origin_left, corner_left]) == 4:
                continue
            if len(neighbours[origin_right, corner_right]) == 4:
                continue

            # Find the direction from each of the two neighbour corners to the other
            # By rotating their direction to the original one.
            step_left_to_right = 1j * step_from_left
            step_right_to_left = -1j * step_from_right

            # Stitch together the whole edge
            for n in range(N):
                offset_left = corner_left - n * step_from_left
                offset_right = corner_right - n * step_from_right
                point_left = (origin_left, offset_left)
                point_right = (origin_right, offset_right)
                neighbours[point_left][step_left_to_right] = (*point_right, step_right_to_left)
                neighbours[point_right][step_right_to_left] = (*point_left, step_left_to_right)

    return {
        (origin + offset, step): (neigh_origin + neigh_offset, neigh_step)
        for (origin, offset), neighs in neighbours.items()
        for step, (neigh_origin, neigh_offset, neigh_step) in neighs.items()
    }


def get_neighbour_map_1(spaces):
    N = get_size(spaces)

    neighbours = {}
    for pos in spaces:
        for step in [1, -1, 1j, -1j]:
            if pos + step in spaces:
                neigh = pos + step
            else:
                i = 1
                while pos - N * i * step in spaces:
                    i += 1
                neigh = pos - (N * i - 1) * step
            neighbours[pos, step] = (neigh, -step)
    return neighbours


def parse_path(text):
    path = []
    for x in text.replace("R", " R ").replace("L", " L ").split():
        path.append(int(x) if x.isdigit() else x)
    return path


def parse_input(text):
    board_text, path_text = text.split("\n\n")
    spaces = {
        complex(c, r): cell
        for r, row in enumerate(board_text.splitlines())
        for c, cell in enumerate(row)
        if cell != " "
    }
    path = parse_path(path_text)
    return spaces, path


def get_start(spaces):
    y = min(z.imag for z in spaces)
    x = [z.real for z in spaces if z.imag == y]
    return min(x) + 1j * y, INITIAL_DIRECTION


def traverse(pos, step, path, spaces, neighbours):
    for instruction in path:
        if instruction in ["R", "L"]:
            step *= {"R": 1j, "L": -1j}[instruction]
        else:
            for _ in range(instruction):
                neigh, negative_step = neighbours[pos, step]
                if spaces[neigh] == "#":
                    break
                pos = neigh
                step = -negative_step
    return pos, step


def compute_password(position, step):
    row_part = 1000 * (1 + int(position.imag))
    col_part = 4 * (1 + int(position.real))
    dir_part = [1, 1j, -1, -1j].index(step)
    return row_part + col_part + dir_part


def solve(text):
    spaces, path = parse_input(text)
    start, step = get_start(spaces)
    yield compute_password(*traverse(start, step, path, spaces, get_neighbour_map_1(spaces)))
    yield compute_password(*traverse(start, step, path, spaces, get_neighbour_map_2(spaces)))


if __name__ == "__main__":
    from helpers import main_template

    main_template("22", solve)
