"""Rock Paper Scissors"""

def solve(text):
    matches = [line.strip().split() for line in text.splitlines()]
    strategy = [(" ABC".find(s1), " XYZ".find(s2)) for s1, s2 in matches]
    points_1 = [shape_2 + ((1 + shape_2 - shape_1) % 3) * 3 for shape_1, shape_2 in strategy]
    yield sum(points_1)
    points_2 = [1 + (shape_1 + outcome) % 3 + (outcome - 1) * 3 for shape_1, outcome in strategy]
    yield sum(points_2)
