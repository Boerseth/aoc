def parse(line):
    return 0


with open("input_1", "r") as f:
    data = [parse(line) for line in f.readlines()]
