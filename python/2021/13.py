"""Transparent Origami"""

def fold(points, fold_direction, fold_coord):
    if fold_direction == "x":
        return {(fold_coord - abs(fold_coord - x), y) for x, y in points}
    return {(x, fold_coord - abs(fold_coord - y)) for x, y in points}




def solve(text):
    lines = [line.strip() for line in text.splitlines() if line.strip()]

    coordinates = set()
    folds = []
    for line in lines:
        if line.startswith("fold along"):
            fold_dir, fold_coord = line.split()[2].split("=")
            folds.append((fold_dir, int(fold_coord)))
        else:
            x, y = line.strip().split(",")
            coordinates.add((int(x), int(y)))
    yield len(fold(coordinates, *folds[0]))


    for f in folds:
        coordinates = fold(coordinates, *f)
    N = 1 + max(x for x, _ in coordinates)
    M = 1 + max(y for _, y in coordinates)
    yield "\n" + "\n".join("".join("#" if (x, y) in coordinates else " " for x in range(N)) for y in range(M))
