"""Trick Shot"""


def solve(text):
    _, target = text.split(": ")
    xmin, xmax, ymin, ymax = [int(v) for word in target.split(", ") for v in word[2:].split("..")]

    yield (ymin**2 - abs(ymin)) // 2

    def is_in(x, y):
        return xmin <= x <= xmax and ymin <= y <= ymax

    heatmap = [[0 for _ in range(xmax + 1)] for __ in range(ymin, abs(ymin) + 1)]
    hits = set()
    for u0 in range(xmax + 1):
        for v0 in range(ymin, abs(ymin) + 1):
            n = 0
            while n < 5 * max(abs(ymin), abs(ymax)) + 1:
                if n > u0:
                    x = (u0 * u0 + u0) // 2
                else:
                    x = n * u0 - (n * n - n) // 2
                y = n * v0 - (n * n - n) // 2
                if is_in(x, y):
                    hits.add((u0, v0))
                    heatmap[ymin - v0][u0] = 1
                    break
                if x > xmax or y < ymin:
                    break
                n += 1

    yield len(hits)


# import matplotlib.pyplot as plt
# plt.imshow(heatmap)
# plt.show()


"""
def get_all_n_and_v0_passing_through(y):
    for n in range(1, 2 * abs(y) + 1, step=2):
        if n % 2 == 0:
            m = n // 2
            if y % m == 0:
                if ((y // m) + n - 1) % 2 == 0:
                    yield n, ((y // m) + n - 1) // 2
        else:
            if y % n == 0:
                m = (n - 1) // 2
                yield n, (y // n) + m


hits = set()
for x, y in [
    (x, y) for x in range(xmin, xmax + 1) for y in range(ymin, ymax + 1)
]:
    for n, v0 in get_all_n_and_v0_passing_through(y):
        if (n * n + n) // 2 < x:
            if n % 2 == 0:
                m = n // 2
                if x % m == 0:
                    if (
        else:
            rad = int((x // 2) ** 0.5)
            if (rad * (rad + 1)) // 2 == x:
                if n >= rad:
                    hits.add((rad, y))
                    continue


        hits.add(??)

"""
