def cache(inner):
    _cache = {}
    def outer(*args):
        if args not in _cache:
            _cache[args] = inner(*args)
        return _cache[args]

    return outer


def multiply(numbers: list[int]) -> int:
    if not numbers:
        return 1
    return numbers.pop() * multiply(numbers)


def get_visible_indices(indexed_trees):
    visible = []
    for i, tree in indexed_trees:
        if not visible or tree > visible[-1][0]:
            visible.append((tree, i))
    return visible



def solve():
    with open("inputs/8", "r") as f:
        text = f.read()
    trees = [[int(t) for t in row] for row in text.splitlines()]
    R = len(trees)
    C = len(trees[0])


    tree_rows = trees
    tree_cols = [list(c) for c in zip(*trees)]
    visible = set()
    for r, tree_row in enumerate(tree_rows):
        visible.update((r, c) for _, c in get_visible_indices(enumerate(tree_row)))
        visible.update((r, c) for _, c in get_visible_indices(reversed(list(enumerate(tree_row)))))

    for c, tree_col in enumerate(tree_cols):
        visible.update((r, c) for _, r in get_visible_indices(enumerate(tree_col)))
        visible.update((r, c) for _, r in get_visible_indices(reversed(list(enumerate(tree_col)))))



    #for r in range(R):
    #    for c in range(C):
    #        tree = tree_rows[r][c]
    #        if (
    #            all(other_tree < tree for other_tree in tree_rows[r][:c])
    #            or all(other_tree < tree for other_tree in tree_rows[r][c + 1 :])
    #            or all(other_tree < tree for other_tree in tree_cols[c][:r])
    #            or all(other_tree < tree for other_tree in tree_cols[c][r + 1 :])
    #        ):
    #            visible_positions.add((r, c))
    yield len(visible_positions)


    @cache
    def get_view_distance(r, c, dr, dc):
        if not (0 <= r + dr < R and 0 <= c + dc < C):
            return 0
        distance = 1
        while (
            trees[r][c] > trees[r + dr * distance][c + dc * distance]
            and 0 <= r + dr * (distance + 1) < R
            and 0 <= c + dc * (distance + 1) < C
        ):
            distance += get_view_distance(r + dr * distance, c + dc * distance, dr, dc)
        return distance


    yield max(
        get_view_distance(r, c, -1, 0) * get_view_distance(r, c, 1, 0) * get_view_distance(r, c, 0, -1) * get_view_distance(r, c, 0, 1)
        for r in range(R) for c in range(C)
    )


def solutions():
    yield 1546
    yield 519064


if __name__ == "__main__":
    from helpers import main_template

    main_template(solve, solutions, with_timer=True)
