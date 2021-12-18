instructions = open("input_1", "r").readline()

# Part 1
print("Part 1:", sum(1 if c == "(" else -1 if c == ")" else 0 for c in instructions))


# Part 2
i = 1
while sum(1 if c == "(" else -1 if c == ")" else 0 for c in instructions[:i]) != -1:
    i += 1
print("Part 2:", i)
