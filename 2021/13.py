lines = [line.strip() for line in open("input_13", "r").readlines() if line.strip()]

coordinates = []
folds = []
for line in lines:
    if line.startswith("fold along"):
        fold_axis, fold_coord = line.split()[2].split("=")
        folds.append((fold_axis, int(fold_coord)))
    else:
        x, y = line.split(",")
        coordinates.append((int(x), int(y)))


def fold_sheet(points, fold_dir, fold_coord):
    if fold_dir == "x":
        return {(fold_coord - abs(fold_coord - x), y) for x, y in points}
    return {(x, fold_coord - abs(fold_coord - y)) for x, y in points}


print("Part 1:", len(fold_sheet(coordinates, *folds[0])))


for fold in folds:
    coordinates = fold_sheet(coordinates, *fold)
X = 1 + max(x for x, _ in coordinates)
Y = 1 + max(y for _, y in coordinates)

print("Part 2:")
print("\n".join("".join("#" if (x, y) in coordinates else " " for x in range(X)) for y in range(Y)))
