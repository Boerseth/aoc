BRACKET_MATCH = {")": "(", "]": "[", "}": "{", ">": "<"}


def find_corruption_score(line):
    error_points = {")": 3, "]": 57, "}": 1197, ">": 25137}
    seen_so_far = []
    for c in line:
        if c not in BRACKET_MATCH:
            # c is an opener
            seen_so_far.append(c)
        elif seen_so_far.pop(-1) != BRACKET_MATCH[c]:
            return error_points[c]
    return 0


def find_completion_score(line):
    completion_points = {"(": 1, "[": 2, "{": 3, "<": 4}
    seen_so_far = []
    for c in line:
        if c not in BRACKET_MATCH:
            # c is an opener
            seen_so_far.append(c)
        else:
            seen_so_far.pop(-1)

    total = 0
    for c in reversed(seen_so_far):
        total *= 5
        total += completion_points[c]
    return total


def solve():
    data = [line.strip() for line in open("inputs/10", "r").readlines()]
    yield sum(find_corruption_score(line) for line in data)
    incomplete_lines = [line for line in data if find_corruption_score(line) == 0]
    sorted_scores = sorted([find_completion_score(line) for line in incomplete_lines])
    yield sorted_scores[len(sorted_scores) // 2]


def solutions():
    yield 296535
    yield 4245130838


if __name__ == "__main__":
    from helpers import main_template

    main_template(solve, solutions)
