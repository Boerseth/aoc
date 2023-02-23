"""Beacon Exclusion Zone"""


def parse_coords(string: str) -> complex:
    coords = string.split(" at ")[1].split(", ")
    x = int(coords[0].split("=")[1])
    y = int(coords[1].split("=")[1])
    return x + y * 1j


def parse(text: str) -> list[list[complex]]:
    lines = text.splitlines()
    return [[parse_coords(c) for c in l.split(": ")] for l in lines]


def manhattan(z: complex) -> int:
    return int(abs(z.real) + abs(z.imag))


def intervals_overlap(min1, max1, min2, max2):
    return not (max2 < min1 or max1 < min2)


def find_covered_intervals_in_row(row, sorted_sensor_reach):
    intervals = []
    for sensor, reach in sorted_sensor_reach:
        if (offset := int(abs((sensor - row).imag))) >= reach:
            continue

        center = int(sensor.real)
        radius = reach - offset
        interval = (center - radius, center + radius)

        overlapping = [interval] + [i for i in intervals if intervals_overlap(*interval, *i)]
        intervals = [i for i in intervals if not intervals_overlap(*interval, *i)]

        starts, ends = zip(*overlapping)
        intervals.append((min(starts), max(ends)))

    return intervals


# All points z on the same declining 45-degree diagonal will have the same
# value from this function. It is an invariant for such points.
def dec_invariant(z):
    return z.real + z.imag


# All points z on the same inclining 45-degree diagonal, etc.
def inc_invariant(z):
    return z.real - z.imag


def sign(x):
    return (x > 0) - (x < 0)


def find_point_between_kissing_sensors(sensor_reach_map):
    distances = {}
    sensor_reaches = list(sensor_reach_map.items())
    for i, (si, ri) in enumerate(sensor_reaches):
        for j, (sj, rj) in enumerate(sensor_reaches[i + 1 :], i + 1):
            key = manhattan(si - sj) - ri - rj
            distances[key] = distances.get(key, []) + [(si, ri, sj, rj)]

    # if not 2 in distances or len(set(distances[2])) != 2:
    #     raise Exception
    (s1, r1, s2, _), (s3, r3, s4, _) = set(distances[2])
    # delta_21 = s2 - s1
    # delta_43 = s4 - s3
    # assert delta_21.real * delta_21.imag * delta_43.real * delta_43.imag < 0

    arbitrary_point_on_interface_1_2 = s1 + r1 * sign((s2 - s1).real)
    arbitrary_point_on_interface_3_4 = s3 + r3 * sign((s4 - s3).real)

    if 0 < sign((s2 - s1).real * (s2 - s1).imag):
        # The line from scanners s1 to s2 is an inclining diagonal,
        # so the interface between their scan-areas will be a
        # _declining_ diagonal.
        # Similarly, the interface 3-4 will need to be an
        # _inclining_ diagonal.
        arbitrary_point_on_declining_diagonal = arbitrary_point_on_interface_1_2
        arbitrary_point_on_inclining_diagonal = arbitrary_point_on_interface_3_4
    else:
        # Otherwise, the situation described above is reversed
        arbitrary_point_on_declining_diagonal = arbitrary_point_on_interface_3_4
        arbitrary_point_on_inclining_diagonal = arbitrary_point_on_interface_1_2
    dec = dec_invariant(arbitrary_point_on_declining_diagonal)
    inc = inc_invariant(arbitrary_point_on_inclining_diagonal)
    # The point  z  at the intersection will both satisfy
    #       dec_invariant(z) == dec
    #       inc_invariant(z) == inc
    #       z = a + ib  =>  dec = a + b,    inc = a - b
    #
    # But this is a matrix system,  z = Av  , with
    #       v = [dec    A = [[1  1]
    #            inc]        [1 -1]]
    # So,
    #       z = A.inv v = 0.5 [[1  1]  [dec     = 0.5 * [dec + inc
    #                          [1 -1]]  inc]             dec - inc]
    # or in complex number notation again,
    #       z = a + ib = (dec + inc)/2 + i(dec - inc)/2
    return complex(dec + inc, dec - inc) / 2


def solve(text):
    sensor_beacon_pair = parse(text.strip())
    sensor_reach = {sensor: manhattan(sensor - beacon) for sensor, beacon in sensor_beacon_pair}
    sorted_sensor_reach = sorted(sensor_reach.items(), key=lambda sr: sr[0].real)
    row = 2000000 * 1j
    yield sum(end - start for start, end in find_covered_intervals_in_row(row, sorted_sensor_reach))

    beacon_location = find_point_between_kissing_sensors(sensor_reach)
    limit = 4000000
    # assert 0 <= beacon_location.real <= limit and 0 <= beacon_location.imag <= limit
    tuning_frequency = int(beacon_location.real * limit + beacon_location.imag)
    yield tuning_frequency
