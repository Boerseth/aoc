with open("input_1", "r") as f:
    data = [int(line) for line in f.readlines()]


def count_decreases(depths, neighbour=1):
    return sum(1 for d1, d2 in zip(depths, depths[neighbour:]) if d1 < d2)


# Part 1
print(count_decreases(data))


# Part 2
print(count_decreases(data, neighbour=3))


