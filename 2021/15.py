risk_level = [[int(c) for c in line.strip()] for line in open("input_15", "r").readlines()]
R = len(risk_level)
C = len(risk_level[0])

path_length = [[None for _ in range(C)] for __ in range(R)]
path_length[-1][-1] = 0


def neighbours(r, c):
    for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        if 0 <= r + dr < R and 0 <= c + dc < C:
            yield r + dr, c + dc


for r, c in ((r, c) for r in reversed(range(R)) for c in reversed(range(C))):
    for rn, cn in neighbours(r, c):
        if path_length[rn][cn] is not None:
            if path_length[r][c] is None or path_length[r][c] > path_length[rn][cn] + risk_level[rn][cn]:
                path_length[r][c] = path_length[rn][cn] + risk_level[rn][cn]
print(path_length[0][0])




def neighbours(r, c):
    for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        if 0 <= r + dr < 5 * R and 0 <= c + dc < 5 * C:
            yield r + dr, c + dc
risk_level = [[(risk_level[r % R][c % C] + (r // R) + (c // C) - 1) % 9 + 1  for c in range(5 * C)] for r in range(5 * R)]
path_length = [[None for _ in range(5 * C)] for __ in range(5 * R)]
path_length[-1][-1] = 0
for r, c in ((r, c) for r in reversed(range(5 * R)) for c in reversed(range(5 * C))):
    for rn, cn in neighbours(r, c):
        if path_length[rn][cn] is not None:
            if path_length[r][c] is None or path_length[r][c] > path_length[rn][cn] + risk_level[rn][cn]:
                path_length[r][c] = path_length[rn][cn] + risk_level[rn][cn]
for r, c in ((r, c) for r in reversed(range(5 * R)) for c in reversed(range(5 * C))):
    for rn, cn in neighbours(r, c):
        if path_length[r][c] > path_length[rn][cn] + risk_level[rn][cn]:
            path_length[r][c] = path_length[rn][cn] + risk_level[rn][cn]
for r, c in ((r, c) for r in reversed(range(5 * R)) for c in reversed(range(5 * C))):
    for rn, cn in neighbours(r, c):
        if path_length[r][c] > path_length[rn][cn] + risk_level[rn][cn]:
            path_length[r][c] = path_length[rn][cn] + risk_level[rn][cn]
for r, c in ((r, c) for r in reversed(range(5 * R)) for c in reversed(range(5 * C))):
    for rn, cn in neighbours(r, c):
        if path_length[r][c] > path_length[rn][cn] + risk_level[rn][cn]:
            path_length[r][c] = path_length[rn][cn] + risk_level[rn][cn]
for r, c in ((r, c) for r in reversed(range(5 * R)) for c in reversed(range(5 * C))):
    for rn, cn in neighbours(r, c):
        if path_length[r][c] > path_length[rn][cn] + risk_level[rn][cn]:
            path_length[r][c] = path_length[rn][cn] + risk_level[rn][cn]
for r, c in ((r, c) for r in reversed(range(5 * R)) for c in reversed(range(5 * C))):
    for rn, cn in neighbours(r, c):
        if path_length[r][c] > path_length[rn][cn] + risk_level[rn][cn]:
            path_length[r][c] = path_length[rn][cn] + risk_level[rn][cn]
for r, c in ((r, c) for r in reversed(range(5 * R)) for c in reversed(range(5 * C))):
    for rn, cn in neighbours(r, c):
        if path_length[r][c] > path_length[rn][cn] + risk_level[rn][cn]:
            path_length[r][c] = path_length[rn][cn] + risk_level[rn][cn]
for r, c in ((r, c) for r in reversed(range(5 * R)) for c in reversed(range(5 * C))):
    for rn, cn in neighbours(r, c):
        if path_length[r][c] > path_length[rn][cn] + risk_level[rn][cn]:
            path_length[r][c] = path_length[rn][cn] + risk_level[rn][cn]
for r, c in ((r, c) for r in reversed(range(5 * R)) for c in reversed(range(5 * C))):
    for rn, cn in neighbours(r, c):
        if path_length[r][c] > path_length[rn][cn] + risk_level[rn][cn]:
            path_length[r][c] = path_length[rn][cn] + risk_level[rn][cn]
for r, c in ((r, c) for r in reversed(range(5 * R)) for c in reversed(range(5 * C))):
    for rn, cn in neighbours(r, c):
        if path_length[r][c] > path_length[rn][cn] + risk_level[rn][cn]:
            path_length[r][c] = path_length[rn][cn] + risk_level[rn][cn]
for r, c in ((r, c) for r in reversed(range(5 * R)) for c in reversed(range(5 * C))):
    for rn, cn in neighbours(r, c):
        if path_length[r][c] > path_length[rn][cn] + risk_level[rn][cn]:
            path_length[r][c] = path_length[rn][cn] + risk_level[rn][cn]
print(path_length[0][0])
