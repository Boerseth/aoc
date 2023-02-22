def find_shortest_path_length(risk_level, R, C):
    path_length = {(0, 0): 0}

    def forward_neighs(r, c):
        if 0 <= r + 1 < R and 0 <= c < C:
            yield r + 1, c
        if 0 <= r < R and 0 <= c + 1 < C:
            yield r, c + 1

    def backward_neighs(r, c):
        if 0 <= r - 1 < R and 0 <= c < C:
            yield r - 1, c
        if 0 <= r < R and 0 <= c - 1 < C:
            yield r, c - 1

    def forward_neighs_to_update(r, c, new_length):
        for neigh in forward_neighs(r, c):
            if (l := path_length.get(neigh)) is None or l > new_length + risk_level[neigh]:
                yield neigh

    def backward_neighs_to_update(r, c, new_length):
        for neigh in backward_neighs(r, c):
            if path_length[neigh] > new_length + risk_level[neigh]:
                yield neigh

    def neighbour_lengths(r, c):
        for neigh in forward_neighs(r, c):
            if (l := path_length.get(neigh)) is not None:
                yield l
        for neigh in backward_neighs(r, c):
            yield path_length[neigh]

    needs_updating = {1: {(1, 0), (0, 1)}}
    # needs_updating is a dict of diagonals:
    # - keys being sum (r+c)
    # - value being sets of (r,c) pairs that for sure need to be updated.
    # Keys/values are popped, so when empty, job is done.
    while needs_updating:
        # Update values in furthest-back diagonal first
        r_plus_c = min(needs_updating.keys())
        to_be_updated = needs_updating.pop(r_plus_c)
        pending_forward = set()
        pending_backward = set()

        for r, c in to_be_updated:  # sorted(to_be_updated, key=lambda a: a[0]):
            new_length = risk_level[r, c] + min(l for l in neighbour_lengths(r, c))
            path_length[r, c] = new_length
            for rn, cn in forward_neighs_to_update(r, c, new_length):
                pending_forward.add((rn, cn))
            for rn, cn in backward_neighs_to_update(r, c, new_length):
                pending_backward.add((rn, cn))

        if pending_backward:
            if r_plus_c - 1 not in needs_updating:
                needs_updating[r_plus_c - 1] = set()
            needs_updating[r_plus_c - 1] |= pending_backward
        if pending_forward:
            if r_plus_c + 1 not in needs_updating:
                needs_updating[r_plus_c + 1] = set()
            needs_updating[r_plus_c + 1] |= pending_forward

    return path_length[R - 1, C - 1]


def solve(text):
    lines = text.splitlines()
    R = len(lines)
    C = len(lines[0].strip())

    risk_level_1 = {
        (r, c): int(ch) for r, line in enumerate(lines) for c, ch in enumerate(line.strip())
    }
    yield find_shortest_path_length(risk_level_1, R, C)

    risk_level_2 = {
        (r, c): (risk_level_1[(r % R), (c % C)] + (r // R) + (c // C) - 1) % 9 + 1
        for r in range(5 * R) for c in range(5 * C)
    }
    yield find_shortest_path_length(risk_level_2, 5 * R, 5 * C)
