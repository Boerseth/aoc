def walk(directions):
    rooms = [0]
    for direction in directions:
        rooms.append(rooms[-1] + direction)
    return rooms

def solve():
    with open("inputs/3", "r") as f:
        text = f.read().strip()
    directions = [{"^": 1j, ">": 1, "v": -1j, "<": -1}[c] for c in text]

    # How many rooms?
    yield len(set(walk(directions)))
    # How many rooms when split in two?
    yield len(set(walk(directions[::2]) + walk(directions[1::2])))


def solutions():
    yield 2592
    yield 2360


if __name__ == "__main__":
    from helpers import main_template

    main_template(solve, solutions)
