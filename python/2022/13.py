"""Distress Signal"""

from ast import literal_eval


def compare(l1, l2):
    if isinstance(l1, int) and isinstance(l2, int):
        if l1 == l2:
            return None
        return l1 < l2

    if isinstance(l1, list) and isinstance(l2, list):
        for e1, e2 in zip(l1, l2):
            if (comparison := compare(e1, e2)) is not None:
                return comparison
        return compare(len(l1), len(l2))

    if isinstance(l1, int):
        return compare([l1], l2)
    return compare(l1, [l2])


def solve(text):
    pairs = [[literal_eval(l) for l in pair.splitlines()] for pair in text.strip().split("\n\n")]
    yield sum(i for i, (left, right) in enumerate(pairs, 1) if False != compare(left, right))

    packets = [p for pair in pairs for p in pair]
    position_1 = 1 + sum(1 for p in packets if False != compare(p, [[2]]))
    position_2 = 2 + sum(1 for p in packets if False != compare(p, [[6]]))
    yield position_1 * position_2
