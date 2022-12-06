annotated_spaces = """#############
#01.2.3.4.56#
###a#b#c#d###
  #e#q#u#p#
  #########"""

H0, H1, H2, H3, H4, H5, H6 = HALLWAY = "0123456"
A1, A2 = A_ROOM = "ae"
B1, B2 = B_ROOM = "bq"
C1, C2 = C_ROOM = "cu"
D2, D2 = D_ROOM = "dp"
ANTEROOMS = "abcd"
BACKROOMS = "equp"

LEGAL_SPACES = HALLWAY + A_ROOM + B_ROOM + C_ROOM + D_ROOM

DISTANCE = {}
for room_outer, hall_left, hall_right in zip(ANTEROOMS, HALLWAY[1:5], HALLWAY[2:6]):
    DISTANCE[room_outer, hall_left] = 2
    DISTANCE[room_outer, hall_right] = 2
    DISTANCE[hall_left, hall_right] = 2
for room_outer, room_inner in zip(ANTEROOMS + H1 + H5, BACKROOMS + H0 + H6):
    DISTANCE[room_outer, room_inner] = 1
DISTANCE |= {(space_2, space_1): d for (space_1, space_2), d in DISTANCE.items()}

NEIGHBOURS = {}
for space_1, space_2 in distance:
    if space_1 not in NEIGHBOURS:
        NEIGHBOURS[space_1] = []
    if space_2 not in NEIGHBOURS:
        NEIGHBOURS[space_2] = []
    NEIGHBOURS[space_1].append(space_2)
    NEIGHBOURS[space_2].append(space_1)


def parse_diagram(diagram):
    space_contents = {space: None for space in LEGAL_SPACES}
    for maybe_amphipod, maybe_space in zip(amphipod_diagram, annotated_spaces):
        if maybe_amphipod not in "ABCD":
            continue
        assert maybe_space in LEGAL_SPACES
        space_contents[maybe_space] = maybe_amphipod
    return space_contents


def minimum_cost(contents):
    pass


amphipod_diagram = """#############
#...........#
###D#B#D#A###
  #C#C#A#B#
  #########"""

print(parse_diagram(amphipod_diagram))

