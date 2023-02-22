"""Probably a Fire Hazard"""

def parse(line):
    *command, coords_1, _, coords_2 = line.split()
    return " ".join(command), *map(int, coords_1.split(",")), *map(int, coords_2.split(","))


def solve(text):
    directions = [parse(line) for line in text.splitlines()]

    lights_1 = [[False] * 1000 for _ in range(1000)]
    for command, x1, y1, x2, y2 in directions:
        for x in range(min(x1, x2), max(x1, x2) + 1):
            for y in range(min(y1, y2), max(y1, y2) + 1):
                if command == "turn on":
                    lights_1[x][y] = True
                if command == "turn off":
                    lights_1[x][y] = False
                if command == "toggle":
                    lights_1[x][y] = not lights_1[x][y]
    yield sum(1 for row in lights_1 for light in row if light)

    lights_2 = [[0] * 1000 for _ in range(1000)]
    for command, x1, y1, x2, y2 in directions:
        for x in range(min(x1, x2), max(x1, x2) + 1):
            for y in range(min(y1, y2), max(y1, y2) + 1):
                if command == "turn on":
                    lights_2[x][y] += 1
                if command == "turn off":
                    lights_2[x][y] = max(0, lights_2[x][y] - 1)
                if command == "toggle":
                    lights_2[x][y] += 2
    yield sum(light for row in lights_2 for light in row if light)

    """
    a = [[1 if light else 0 for light in row] for row in lights_1]
    import matplotlib.pyplot as plt
    plt.imshow(a)
    plt.show()
    plt.imshow(lights_2)
    plt.show()
    """
