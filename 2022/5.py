def parse_diagram(diagram_text):
    diagram_lines = diagram_text.splitlines()[::-1]
    return ["".join(stack).strip() for stack in list(zip(*diagram_lines))[1::4]]


def parse_moves(move_text):
    moves_1_index = [map(int, line.split()[1::2]) for line in move_text.splitlines()]
    return [(n, from_pos - 1, to_pos - 1) for n, from_pos, to_pos in moves_1_index]


def parse(text):
    diagram_end = text.find("\n\n")
    return parse_diagram(text[:diagram_end]), parse_moves(text[diagram_end + 2 :])


def rearrange(stacks, moves, move_multiple=False):
    order = 1 if move_multiple else -1
    for number, from_pos, to_pos in moves:
        stacks[to_pos] += stacks[from_pos][-number:][::order]
        stacks[from_pos] = stacks[from_pos][:-number]
    return stacks


def solve():
    with open("inputs/5", "r") as f:
        text = f.read()
    yield "".join(stack[-1] for stack in rearrange(*parse(text), False))
    yield "".join(stack[-1] for stack in rearrange(*parse(text), True))


def solutions():
    yield "WSFTMRHPP"
    yield "GSLCMFBRP"


if __name__ == "__main__":
    from helpers import main_template

    main_template(solve, solutions)
