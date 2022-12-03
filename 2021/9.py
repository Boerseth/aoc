def neighbours(y, x, N, M):
    for d in [-1, 1]:
        if 0 <= y + d < N:
            yield y + d, x
        if 0 <= x + d < M:
            yield y, x + d


cache = {}
def get_basin(heights, y, x):
    N = len(heights)
    M = len(heights[0])
    if (x, y) not in cache:
        basin = {(y, x)}
        for a, b in neighbours(y, x, N, M):
            if heights[y][x] < heights[a][b] < 9:
                basin |= get_basin(heights, a, b)
        cache[(x, y)] = basin
    return cache[(x, y)]


def solve():
    heights = [[int(c) for c in line.strip()] for line in open("input_9", "r").readlines()]
    N = len(heights)
    M = len(heights[0])

    lowpoints = [
        (y, x) for y in range(N) for x in range(M)
        if all(heights[y][x] < heights[a][b] for a, b in neighbours(y, x, N, M))
    ]
    yield sum(heights[y][x] + 1 for y, x in lowpoints)

    basin_sizes = sorted([len(get_basin(heights, y, x)) for y, x in lowpoints])
    yield basin_sizes[-1] * basin_sizes[-2] * basin_sizes[-3]


def solutions():
    yield 436
    yield 1317792


if __name__ == "__main__":
    from helpers import main_template

    main_template(solve, solutions)
