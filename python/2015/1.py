"""Not Quite Lisp"""


def solve(text):
    instructions = [1 if c == "(" else -1 if c == ")" else 0 for c in text]

    yield sum(instructions)

    partial_sum = 0
    for i, instruction in enumerate(instructions, 1):
        partial_sum += instruction
        if partial_sum == -1:
            break
    yield i
