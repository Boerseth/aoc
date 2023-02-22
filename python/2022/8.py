from functools import cache
from typing import Iterable


def visible_indices_from_one_side(indexed_tree_line: Iterable[tuple[int, int]]) -> list[int]:
    visible_indexed_trees = []
    for i, tree in indexed_tree_line:
        if not visible_indexed_trees or tree > visible_indexed_trees[-1][1]:
            visible_indexed_trees.append((i, tree))
    return [i for i, _ in visible_indexed_trees]


def visible_indices(tree_line: list[int]) -> list[int]:
    indexed_tree_line = list(enumerate(tree_line))
    visible_from_start = visible_indices_from_one_side(indexed_tree_line)
    visible_from_end = visible_indices_from_one_side(reversed(indexed_tree_line))
    return visible_from_start + visible_from_end


class Forest:
    def __init__(self, trees: list[list[int]]) -> None:
        self.trees = trees
        self.R = len(trees)
        self.C = len(trees[0])

    def __getitem__(self, coords):
        r, c, *_ = coords
        return self.trees[r][c]

    @cache
    def get_viewing_distance(self, r, c, dr, dc):
        if not (0 <= r + dr < self.R and 0 <= c + dc < self.C):
            return 0
        distance = 1
        r_n = r + dr * distance
        c_n = c + dc * distance
        while self[r, c] > self[r_n, c_n] and 0 <= r_n + dr < self.R and 0 <= c_n + dc < self.C:
            distance += self.get_viewing_distance(r_n, c_n, dr, dc)
            r_n = r + dr * distance
            c_n = c + dc * distance
        return distance

    def get_scenic_score(self, r, c):
        scenic_score = 1
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            scenic_score *= self.get_viewing_distance(r, c, dr, dc)
        return scenic_score

    def get_visible_tree_coordinates(self) -> set[tuple[int, int]]:
        trees_pivot = map(list, zip(*self.trees))
        return {
            *{(r, c) for r, row in enumerate(self.trees) for c in visible_indices(row)},
            *{(r, c) for c, col in enumerate(trees_pivot) for r in visible_indices(col)},
        }


def solve(text):
    forest = Forest([[int(t) for t in row] for row in text.splitlines()])
    yield len(forest.get_visible_tree_coordinates())
    yield max(forest.get_scenic_score(r, c) for r in range(forest.R) for c in range(forest.C))


if __name__ == "__main__":
    from helpers import main_template

    main_template("8", solve)
