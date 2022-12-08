def cache(inner):
    _cache = {}

    def outer(*args):
        if args not in _cache:
            _cache[args] = inner(*args)
        return _cache[args]

    return outer


def visible_indices_from_one_side(indexed_trees):
    visible = []
    for i, tree in indexed_trees:
        if not visible or tree > visible[-1][0]:
            visible.append((tree, i))
    return [i for _, i in visible]


def visible_indices(tree_line):
    visible_from_start = visible_indices_from_one_side(enumerate(tree_line))
    visible_from_end = visible_indices_from_one_side(reversed(list(enumerate(tree_line))))
    return visible_from_start + visible_from_end


def visible_coords_sideways(trees):
    return [(r, c) for r, row in enumerate(trees) for c in visible_indices(row)]


def solve():
    with open("inputs/8", "r") as f:
        text = f.read()
    trees = [[int(t) for t in row] for row in text.splitlines()]
    R = len(trees)
    C = len(trees[0])

    visible_horizontally = visible_coords_sideways(trees)
    visible_vertically = [(r, c) for c, r in visible_coords_sideways(map(list, zip(*trees)))]
    visible = {*visible_horizontally, *visible_vertically}
    yield len(visible)

    @cache
    def view_distance(r, c, dr, dc):
        if not (0 <= r + dr < R and 0 <= c + dc < C):
            return 0
        distance = 1
        r_next = r + dr * distance
        c_next = c + dc * distance
        while trees[r][c] > trees[r_next][c_next] and 0 <= r_next + dr < R and 0 <= c_next + dc < C:
            distance += view_distance(r_next, c_next, dr, dc)
            r_next = r + dr * distance
            c_next = c + dc * distance
        return distance

    def scenic_score(r, c):
        scenic_score = 1
        for _dir in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            scenic_score *= view_distance(r, c, *_dir)
        return scenic_score

    yield max(scenic_score(r, c) for r in range(R) for c in range(C))


def solutions():
    yield 1546
    yield 519064


if __name__ == "__main__":
    from helpers import main_template

    main_template(solve, solutions)
