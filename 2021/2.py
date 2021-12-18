with open("input_2", "r") as f:
    real_lines = f.readlines()

test_lines = """forward 5
down 5
forward 8
up 3
down 8
forward 2""".split("\n")


# Interpret movement as a complex number
# - Has direction and magnitude
# - Can be summed easily
def parse(command):
    if command.startswith("forward"):
        return int(command.split()[1])
    if command.startswith("down"):
        return int(command.split()[1]) * 1j
    if command.startswith("up"):
        return - int(command.split()[1]) * 1j
    raise Exception

test_data = [parse(line) for line in test_lines]
real_data = [parse(line) for line in real_lines]


# Part 1
print((lambda z: z.real * z.imag)(sum(test_data)))
print((lambda z: z.real * z.imag)(sum(real_data)))


# Part 2
# Aims at each step can be computed first, and then zipped with data in a sum:
aims = [sum(real_data[: i + 1]).imag for i in range(len(real_data))]
answer = sum(z.real * (1 + 1j * aim) for z, aim in zip(real_data, aims))
print(answer.real * answer.imag)

"""
aim = 0
depth = 0
hor = 0
for z in real_data:
    aim += z.imag
    hor += z.real
    depth += z.real * aim
print(depth * hor)
"""
