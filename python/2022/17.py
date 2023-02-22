"""Pyroclastic Flow"""

TEST_INPUT = ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"
BYTE = 8

INDENT = 2
HEIGHT = 3
OFFSET = HEIGHT * BYTE - INDENT

BEDROCK = 0b01111111
WALL_BY_ROW = [
    0b10000000,
    0b10000000,
    0b10000000,
    0b10000000,
    0b10000000,
    0b10000000,
    0b10000000,
    0b10000000,
]
WALL = sum(row << (i * BYTE) for i, row in enumerate(WALL_BY_ROW))

ROCKS_BY_ROW = [
    [
        0b01111000,
    ],
    [
        0b00100000,
        0b01110000,
        0b00100000,
    ],
    [
        0b00010000,
        0b00010000,
        0b01110000,
    ],
    [
        0b01000000,
        0b01000000,
        0b01000000,
        0b01000000,
    ],
    [
        0b01100000,
        0b01100000,
    ],
]
ROCKS = [
    sum(row << (OFFSET + i * BYTE) for i, row in enumerate(reversed(rock))) for rock in ROCKS_BY_ROW
]


def chamber_to_string(chamber):
    lines = []
    while chamber:
        lines.append("{0:08b}".format(chamber % 2**BYTE).replace("1", "#").replace("0", "."))
        chamber >>= BYTE
    return "\n".join(reversed(lines))


def top_n_rows(chamber, n):
    # There is an inbuild off-by-one error here: should have +1
    # This is because of the bedrock layer I add to chamber.
    roll = (chamber.bit_length() // BYTE) - n + 1
    if roll > 0:
        return chamber >> roll * BYTE
    if roll < 0:
        return chamber << abs(roll) * BYTE
    return chamber


def apply_move(rock, move):
    if move == "<":
        return rock << 1
    if move == ">":
        return rock >> 1
    assert False


def overlaps(int1, int2):
    return bool(int1 & int2)


def iterate(iterable):
    while True:
        yield from iterable


def get_n_rocks(N):
    for n, rock in enumerate(iterate(ROCKS)):
        yield ROCKS[n % 5]
        if n == N - 1:
            break


def shift_rows(rock, n):
    if n > 0:
        return rock << (BYTE * n)
    if n < 0:
        return rock >> (BYTE * abs(n))
    return rock


def shift_rock(rock, chamber, fall_depth):
    chamber_height = chamber.bit_length() // BYTE
    return shift_rows(rock, chamber_height - fall_depth)


def place_rock_in_chamber(chamber, rock, fall_depth):
    rock_shifted = shift_rows(rock, (chamber.bit_length() // BYTE) - fall_depth)
    return chamber | rock_shifted


def simulate(moves, n):
    chamber = BEDROCK
    for rock in get_n_rocks(n):
        fall_depth = 0
        chamber_top_part = top_n_rows(chamber, 0)
        assert chamber_top_part == 0
        while not overlaps(rock, chamber_top_part):
            move = next(moves)
            moved_rock = apply_move(rock, move)
            if not overlaps(moved_rock, WALL | chamber_top_part):
                rock = moved_rock
            fall_depth += 1
            chamber_top_part = top_n_rows(chamber, fall_depth)
        fall_depth -= 1
        rock_shifted = shift_rows(rock, (chamber.bit_length() // BYTE) + 1 - fall_depth)
        assert not (rock_shifted & chamber)
        chamber += rock_shifted
    return chamber


def find_cycle(text):
    M = len(text)
    m = 0
    r = 0
    previous_height = {(0, 0): 0}
    encountered_states = {}
    moves = enumerate(iterate(list(enumerate(text))))
    rocks = enumerate(iterate(list(enumerate(ROCKS))))

    chamber = BEDROCK
    while True:
        r, (ri, rock) = next(rocks)

        fall_depth = 0
        chamber_top_part = top_n_rows(chamber, 0)
        assert chamber_top_part == 0

        while not overlaps(rock, chamber_top_part):
            m, (mi, move) = next(moves)
            moved_rock = apply_move(rock, move)
            if not overlaps(moved_rock, WALL | chamber_top_part):
                rock = moved_rock
            fall_depth += 1
            chamber_top_part = top_n_rows(chamber, fall_depth)
        fall_depth -= 1
        rock_shifted = shift_rows(rock, (chamber.bit_length() // BYTE) + 1 - fall_depth)
        assert not (rock_shifted & chamber)
        chamber += rock_shifted

        state_i = (ri, mi)
        h_curr = chamber.bit_length() // BYTE
        if state_i not in previous_height:
            previous_height[ri, mi] = h_curr
            continue
        h_prev = previous_height[state_i]
        previous_height[ri, mi] = h_curr

        chamber_since_previous = top_n_rows(chamber, h_curr - h_prev)
        state = (chamber_since_previous, ri, mi)
        if state not in encountered_states:
            encountered_states[state] = r
            continue
        r_prev = encountered_states[state]
        T = r - r_prev
        p = r_prev
        return T, p


def get_height(text, n):
    chamber = simulate(iterate(text), n)
    chamber_height = chamber.bit_length() // BYTE
    return chamber_height


def solve(text):
    text = text.strip()
    # text = TEST_INPUT
    def h(n):
        return get_height(text, n)

    yield h(2022)

    # Because this is a cyclical pattern of M moves and R rocks,
    # There will be some point where the building pattern repeats
    # every T rocks.
    # It's not clear how long it will take for the pattern to get
    # going, but it shouldn't be too long. Call the number of
    # moves before the pattern starts  p  and we have a function
    # for height that is linear,
    #       h(x) = h(p + ((x - p) % T)) + (h(p + T) - h(p)) * ((x - p) // T)
    T, p = find_cycle(text)
    x = 1_000_000_000_000
    dh_rep = h(p + T) - h(p)
    rep_num = (x - p) // T
    rep_mod = (x - p) % T
    h_p_plus_mod = h(p + rep_mod)
    yield h_p_plus_mod + dh_rep * rep_num
