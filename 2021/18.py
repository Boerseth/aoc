def left_add(p, l):
    if isinstance(p, int):
        return p + l
    return [p[0], left_add(p[1], l)]


def right_add(p, r):
    if isinstance(p, int):
        return p + r
    return [right_add(p[0], r), p[1]]


def explode(p, i):  # Returns tuple (left_add, right_add, did_explode, value)
    if isinstance(p, int):
        return 0, 0, False, p
    p0, p1 = p
    if i == 4:
        return p0, p1, True, 0
    l0, r0, did_explode, p0 = explode(p0, i + 1)
    if not did_explode:
        l1, r1, did_explode, p1 = explode(p1, i + 1)
        if not did_explode:
            return 0, 0, False, p
        if l1 != 0:
            p0 = left_add(p0, l1)
        return 0, r1, did_explode, [p0, p1]
    if r0 != 0:
        p1 = right_add(p1, r0)
    return l0, 0, did_explode, [p0, p1]


def split(p, has_already_split):
    if has_already_split:
        return True, p
    if isinstance(p, int):
        return (True, [p//2, (p + 1)//2]) if p >= 10 else (False, p)
    p0, p1 = p
    has_already_split, p0 = split(p0, has_already_split)
    has_already_split, p1 = split(p1, has_already_split)
    return has_already_split, [p0, p1]


def add_pairs(p1, p2):
    p = [p1, p2]
    while True:
        _, _, did_explode, p_reduced = explode(p, 0)
        if did_explode:
            p = p_reduced
            continue
        did_split, p_split = split(p, False)
        if did_split:
            p = p_split
            continue
        break
    return p


def magnitude(p):
    return p if isinstance(p, int) else 3 * magnitude(p[0]) + 2 * magnitude(p[1])


def solve(text):
    pairs = [eval(line) for line in text.splitlines()]
    snail_sum = pairs[0]
    for pair in pairs[1:]:
        snail_sum = add_pairs(snail_sum, pair)

    yield magnitude(snail_sum)
    yield max(magnitude(add_pairs(p1, p2)) for p1 in pairs for p2 in pairs)


if __name__ == "__main__":
    from helpers import main_template

    main_template("18", solve)
