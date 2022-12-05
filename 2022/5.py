def parse_input(text):
    end = text.find("\n 1")
    diagram_lines, move_lines = text[:end].splitlines(), text[end:].splitlines()[3:]
    crates = [list("".join(stack).strip()) for stack in list(zip(*diagram_lines[::-1]))[1::4]]
    moves_1_indexed = [map(int, line.split()[1::2]) for line in move_lines]
    moves = [(num, from_pos - 1, to_pos - 1) for num, from_pos, to_pos in moves_1_indexed]
    return crates, moves


def rearrange_crates(crate_stacks, move_steps, move_multiple=False):
    order = 1 if move_multiple else -1
    for number, from_pos, to_pos in move_steps:
        crate_stacks[to_pos] += crate_stacks[from_pos][-number:][::order]
        crate_stacks[from_pos] = crate_stacks[from_pos][:-number]
    return "".join(c[-1] for c in crate_stacks)


def solve():
    with open("inputs/5", "r") as f:
        text = f.read()
    crate_stacks, move_steps = parse_input(text)
    yield rearrange_crates([[c for c in s] for s in crate_stacks], move_steps, move_multiple=False)
    yield rearrange_crates([[c for c in s] for s in crate_stacks], move_steps, move_multiple=True)


def solutions():
    yield "WSFTMRHPP"
    yield "GSLCMFBRP"


if __name__ == "__main__":
    from helpers import main_template

    main_template(solve, solutions)
