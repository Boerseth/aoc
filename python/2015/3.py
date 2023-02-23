"""Perfectly Spherical Houses in a Vacuum"""


def walk(directions):
    rooms = [0]
    for direction in directions:
        rooms.append(rooms[-1] + direction)
    return rooms


def solve(text):
    text = text.strip()
    directions = [{"^": 1j, ">": 1, "v": -1j, "<": -1}[c] for c in text]

    # How many rooms?
    yield len(set(walk(directions)))
    # How many rooms when split in two?
    yield len(set(walk(directions[::2]) + walk(directions[1::2])))
