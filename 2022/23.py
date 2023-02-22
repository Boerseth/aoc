def neighbours(z):
    for dz in [1, 1 + 1j]:
        for rot in [1, 1j, -1, -1j]:
            yield z + dz * rot


def disperse(elves):
    proposed = {}
    for elf, directions in list(elves.items()):
        elves[elf] = directions[1:] + directions[:1]

        if not any(neigh in elves for neigh in neighbours(elf)):
            continue  # Elf must have some neighbours
        if all(any(elf + pos in elves for pos in dir_) for dir_ in directions):
            continue  # Elf must have an open direction
        direction = next(dir_ for dir_ in directions if not any(elf + pos in elves for pos in dir_))
        proposal = elf + direction[0]

        if proposal in proposed:
            # Block all elves from entering this, since multiple are trying
            proposed[proposal] = None
            continue

        proposed[proposal] = elf

    # Filter None values due to collisions
    proposed = {pos: elf for pos, elf in proposed.items() if elf is not None}
    for position, elf in proposed.items():
        elves[position] = elves.pop(elf)

    return elves, len(proposed)


def get_area(elves):
    xvals = [int(elf.real) for elf in elves]
    yvals = [int(elf.imag) for elf in elves]
    xmin, xmax = min(xvals), max(xvals)
    ymin, ymax = min(yvals), max(yvals)
    return (xmax - xmin + 1) * (ymax - ymin + 1)


def get_directions():
    return [
        [complex(0, 1), complex(1, 1), complex(-1, 1)],
        [complex(0, -1), complex(1, -1), complex(-1, -1)],
        [complex(-1, 0), complex(-1, 1), complex(-1, -1)],
        [complex(1, 0), complex(1, 1), complex(1, -1)],
    ]


def parse(text):
    return {
        complex(i, j): get_directions()
        for j, line in enumerate(reversed(text.splitlines()))
        for i, char in enumerate(line)
        if char == "#"
    }


def solve(text):
    elves = parse(text)
    for _ in range(10):
        elves, _ = disperse(elves)
    yield get_area(elves) - len(elves)

    elves = parse(text)
    round_count = 0
    moves = -1
    while moves:
        round_count += 1
        elves, moves = disperse(elves)
    yield round_count


if __name__ == "__main__":
    from helpers import main_template

    main_template("23", solve)
