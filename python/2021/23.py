"""Amphipod"""

ROOM_NUMBER = {"A": 3, "B": 5, "C": 7, "D": 9}
POSITIONS = [
    *[(1, i) for i in range(1, 12)],
    *[(2, i) for i in range(3, 10, 2)],
    *[(3, i) for i in range(3, 10, 2)],
]


def print_diagram(diagram):
    print("\n".join(map("".join, zip(*[iter(diagram)] * 13))))


def get_index(position):
    r, c = position
    return c + 13 * r


# Sanity check:
amphipod_diagram = list("""#############
#...........#
###B#C#B#D###
  #A#D#C#A#  
  #########  """.replace("\n", ""))
amphipod_diagram = list("""#############
#...........#
###D#B#D#A###
  #C#C#A#B#  
  #########  """.replace("\n", ""))
assert all(amphipod_diagram[get_index(pos)] != "#" for pos in POSITIONS)


def is_move_legal(diagram, amphipod, origin, destination):
    r_orig, c_orig = origin
    r_dest, c_dest = destination
    return not (
        # Should never happen but
        (origin == destination)
        # Don't move from one hallway spot to another
        or (r_orig == 1 and r_dest == 1)
        # Don't stop in the hallway if it's not between rooms
        or (r_dest == 1 and diagram[get_index((2, c_dest))] != "#")
        # Don't move into a room if not their own
        or (r_dest >= 2 and c_dest != ROOM_NUMBER[amphipod])
        # Don't move into outer part of own room if partner not already in inner part
        or (r_dest == 2 and diagram[get_index((3, c_dest))] != amphipod)
        # Never just move from inner to outer part of room
        or (r_dest == 2 and r_orig == 3 and c_dest == c_orig)
        # Don't move if in a completed room
        or (c_orig == ROOM_NUMBER[amphipod] and diagram[get_index((2, c_orig))] == diagram[get_index((3, c_orig))] == amphipod)
        # Don't move out if you're alone at home inner
        or (c_orig == ROOM_NUMBER[amphipod] and r_orig == 3)
        # Otherwise, should be fine...
    )


def _get_legal_destinations(diagram, amphipod, origin, previous, current, distance):
    r_orig, c_orig = origin
    r_curr, c_curr = current

    legal_destinations = []
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        destination = (r_curr + dr, c_curr + dc)

        # Skip if backwards
        if previous == destination:
            continue
        # Skip if blocked
        if diagram[get_index(destination)] != ".":
            continue

        if is_move_legal(diagram, amphipod, origin, destination):
            legal_destinations.append((destination, distance + 1))

        legal_destinations += _get_legal_destinations(
            diagram, amphipod, origin, current, destination, distance + 1
        )
    return legal_destinations


def can_go_straight_home(diagram, amphipod, pos):
    r, c = pos
    c_room = 

def get_hallway_positions_incr(start, end):
    if start <= 1:
        yield 1
    i = 2
    while i <= end:
        yield i
        i += 2
    if end == 11:
        yield 11


def get_hallway_positions_decr(start, end):
    if start >= 11:
        yield 11
    i = 10
    while i >= end:
        yield i
        i -= 2
    if end <= 1:
        yield 1

def get_legal_destinations(diagram, max_depth, amphipod, pos):
    r, c = pos
    c_room = ROOM_NUMBER[amphipod]
    if r > 1:
        range_in_front = range(r - 1, 1, -1)
        if any(diagram[(r_i, c)] != "." for r_i in range_in_front):
            return []
        if c == c_room:
            range_behind = range(1 + max_depth, r - 1, -1)
            if all(diagram[(r_i, c)] == amphipod for r_i in range_behind):
            return []

        range_right = list(range(c + 1, 11, 2)) + [11]
        range_left = list(range(c - 1, 0, -2)) + [1]
        destinations = []
        for c_i in range_right:
            if diagram[(1, c_i)] != ".":
                break
            destinations.append(((1, c_i), r - 1 + abs(c_i - c)))
        for c_i in range_left:
            if diagram[(1, c_i)] != ".":
                break
            destinations.append(((1, c_i), r - 1 + abs(c_i - c)))
        return destinations
    # r == 1
    range_to_check = (c + 1 + (c > 1), c_room) if c < c_room else (c_room + 1, c)
    for c_i in range(*range_to_check, 2):
        if diagram[(1, c_i)] != ".":
            return []
    for r_i in range(1 + max_depth, 1, -1):
        content = diagram[(r_i, c_room)]
        if content == ".":
            return [((r_i, c_room), r_i - 1 + abs(c_room - c))]
        if content != amphipod:
            return []
    raise Exception(f"seems to be too many of type {amphipod}")



def get_legal_moves(diagram):
    legal_moves = []
    for pos in POSITIONS:
        amphipod = diagram[pos]
        if not amphipod in "ABCD":
            continue
        legal_moves += [(amphipod, pos, dest, dist) for dest, dist in get_legal_destinations(diagram, 2, amphipod, pos)]
    return legal_moves
def _get_legal_moves(diagram):
    legal_moves = []
    for pos in POSITIONS:
        amphipod = diagram[get_index(pos)]
        if not amphipod in "ABCD":
            continue
        legal_moves += [(amphipod, pos, dest, dist) for dest, dist in _get_legal_destinations(diagram, amphipod, pos, pos, pos, 0)]
    return legal_moves


def apply_move(diagram, origin, destination):
    new_diagram = {k: v for k, v in diagram.items()}
    new_diagram[origin] = diagram[destination]
    new_diagram[destination] = diagram[origin]
    return new_diagram

def _apply_move(diagram, origin, destination):
    index_orig = get_index(origin)
    index_dest = get_index(destination)
    amphipod = diagram[index_orig]
    new_diagram = [c for c in diagram]
    new_diagram[index_orig] = "."
    new_diagram[index_dest] = amphipod
    return new_diagram


AMPHIPOD_ENERGY_COST = {
    "A": 1,
    "B": 10,
    "C": 100,
    "D": 1000,
}

def move_cost(amphipod, distance):
    return distance * AMPHIPOD_ENERGY_COST[amphipod]



DONE = list("""#############
#...........#
###A#B#C#D###
  #A#B#C#D#  
  #########  """.replace("\n", ""))

TEST = list("""#############
#A..........#
###.#B#C#D###
  #A#B#C#D#  
  #########  """.replace("\n", ""))

assert TEST == _apply_move([c for c in DONE], (2, 3), (1, 1))
for amphipod, col in ROOM_NUMBER.items():
    assert DONE[get_index((2, col))] == amphipod
    assert DONE[get_index((3, col))] == amphipod


def parse_diagram(text):
    diagram = {}
    for r, line in enumerate(text.splitlines()):
        for c, symbol in enumerate(line):
            if symbol in " #":
                continue
            diagram[(r, c)] = symbol
    return diagram


DONE = parse_diagram("""#############
#...........#
###A#B#C#D###
  #A#B#C#D#  
  #########  """)


cache = {}
def find_minimum_cost(diagram):
    diagram_string = "".join(map(lambda k: str((k, diagram[k])), sorted(diagram.keys())))
    if diagram_string in cache:
        return cache[diagram_string]
    if diagram == DONE:
        return 0, []

    minimum = None
    moves = []

    legal_moves = get_legal_moves(diagram)
    if len(legal_moves) == 0:
        cache[diagram_string] = None, []
        return None, []

    for amphipod, orig, dest, dist in legal_moves:
        minimum_for_move, next_moves = find_minimum_cost(apply_move(diagram, orig, dest))
        if minimum_for_move is None:
            continue
        cost = minimum_for_move + move_cost(amphipod, dist)
        if minimum and cost >= minimum:
            continue
        minimum = cost
        moves = [(orig, dest)] + next_moves

    cache[diagram_string] = minimum, moves
    return minimum, moves

_amphipod_diagram = """#############
#...........#
###D#B#D#A###
  #C#C#A#B#
  #########"""

assert not get_legal_destinations(parse_diagram("""
#.D.........#
###.#B#D#A###
  #C#C#A#B#
  #########"""), 2, "D", (1, 2))
l = get_legal_destinations(parse_diagram("""
#...........#
###C#B#D#B###
  #A#C#A#D#
  #########"""), 2, "C", (2, 3))
assert len(l) == 7

cost, moves = find_minimum_cost(parse_diagram(_amphipod_diagram))
print(cost)
print(moves)


print_diagram(amphipod_diagram)
for orig, dest in moves:
    amphipod_diagram = _apply_move(amphipod_diagram, orig, dest)
    print_diagram(amphipod_diagram)
    print()
