def solve():
    with open("inputs/1", "r") as f:
        text = f.readline()
    instructions = [1 if c == "(" else -1 if c == ")" else 0 for c in text]

    yield sum(instructions)

    partial_sum = 0
    for i, instruction in enumerate(instructions, 1):
        partial_sum += instruction
        if partial_sum == -1:
            break
    yield i


def solutions():
    yield 232
    yield 1783


if __name__ == "__main__":
    from helpers import main_template

    main_template(solve, solutions)
