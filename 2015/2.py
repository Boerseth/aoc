instructions = [sorted([int(num) for num in line.split("x")]) for line in open("input_2", "r").readlines()]


# Part 1
print("Part 1:", sum(3 * x * y + 2 * x * z + 2 * y * z for x, y, z in instructions))


# Part 1
print("Part 1:", sum(2 * x + 2 * y + x * y * z for x, y, z in instructions))
