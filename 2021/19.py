import time
from dataclasses import dataclass
from math import log2

Coord = int
Position = tuple[Coord, Coord, Coord]
Distance = tuple[Coord, Coord, Coord]
Beacon = Position


#     If two scanners overlap, they per def. share 12 beacon
# positions. All these 12 points will have the same distances
# to the 11 other points regardless of perspective, so the
# interdistance-sets must share
#     2 * (11 + 10 + 9 + ... + 2 + 1)
#         = 2 * (12 * (12 - 1) / 2)
#         = 132
# values.
#     All such sets also share the Zero-vector (0, 0, 0), so
# we skip if the two scanners share < 133 distances.
OVERLAP_THRESHOLD = 12
DISTANCE_MATCH_THRESHOLD = 1 + (OVERLAP_THRESHOLD * (OVERLAP_THRESHOLD - 1))
MAX_DIST = 1000

# OPTIMIZATIONS:
CLOSE_NEIGH_CUTOFF_SQUARED = int((2 * MAX_DIST / (OVERLAP_THRESHOLD) ** (1 / 3)) ** 2)
CLOSE_DISTANCE_MATCH_THRESHOLD = 2 * OVERLAP_THRESHOLD

#     Idea:
# Actually, we can do better than the Euclidean distance.
# The Euclidean distance strips away the direction and
# orientation of the sensor readings, so we would still
# have to search through all orientations even when a
# match is found.

#     Improvement:
# Since tuples are hashable, compare sets of delta vecors!
#     Disadvantage:
# We have to compute 24 such distance sets per scanner
# (1 for each orientation) instead of just 1, shifting
# time cost to prep-work instead of matching.
# Still, so long as it is cheaper to compute such a set
# than to compare clusters many times, on average, it will
# save time.
#     Potential further improvement:
# Look for "close pairs" of beacons, and restrict the
# distance set to them. Would require some prep-work on
# beacons per scanner, but significantly reduce the compute
# time on each of the 24 * N distance sets.
# Worst bad-luck case would be all OVELAP_THRESHOLD beacons
# evenly distributed in the whole cube of size
#     (2MAX_DIST x 2MAX_DIST x 2MAX_DIST)
# with the rest squeezed tighly together just outside.
# In this case, the closest neighbour distance would be about
#     2 * MAX_DIST / OVERLAP_THRESHOLD ** 0.33
# So with that as the cutoff for a "close" neighbour, we can
# still expect to find at least 2 * OVERLAP_THRESHOLD number of
# distance matches.
# Might result in some false-positives, but probably not.
# Might also be that the 12 matching points are not in fact 
# "close" by this definition. To be robust, there should be
# some loosening of constraints happening as calibration
# cycles continue without finding matches.


def add(r1, r2):
    x1, y1, z1 = r1
    x2, y2, z2 = r2
    return x1 + x2, y1 + y2, z1 + z2


def diff(r1, r2):
    x1, y1, z1 = r1
    x2, y2, z2 = r2
    return x1 - x2, y1 - y2, z1 - z2


def sq_norm(r):
    x, y, z = r
    return x ** 2 + y ** 2 + z ** 2


def orientations():
    # At first, I did this in a cleverer way, as
    #
    # for permutation in permutations():
    #     for rotation in rotations():
    #         for flip in flips():
    #             yield lambda x, y, z: permutation(*rotation(*flip(x, y, z)))
    #
    # But no-compositions saves like 20% on overall running time.
    # Creating the difference sets is what takes the most time now,
    # so the composed function calls, while elegant, are not optimal.
    yield lambda x, y, z: (x, y, z)
    yield lambda x, y, z: (-y, x, z)
    yield lambda x, y, z: (-x, -y, z)
    yield lambda x, y, z: (y, -x, z)

    yield lambda x, y, z: (-y, -x, -z)
    yield lambda x, y, z: (x, -y, -z)
    yield lambda x, y, z: (y, x, -z)
    yield lambda x, y, z: (-x, y, -z)

    yield lambda x, y, z: (y, z, x)
    yield lambda x, y, z: (x, z, -y)
    yield lambda x, y, z: (-y, z, -x)
    yield lambda x, y, z: (-x, z, y)

    yield lambda x, y, z: (-x, -z, -y)
    yield lambda x, y, z: (-y, -z, x)
    yield lambda x, y, z: (x, -z, y)
    yield lambda x, y, z: (y, -z, -x)

    yield lambda x, y, z: (z, x, y)
    yield lambda x, y, z: (z, -y, x)
    yield lambda x, y, z: (z, -x, -y)
    yield lambda x, y, z: (z, y, -x)

    yield lambda x, y, z: (-z, -y, -x)
    yield lambda x, y, z: (-z, x, -y)
    yield lambda x, y, z: (-z, y, x)
    yield lambda x, y, z: (-z, -x, y)


class ScanData:
    def __init__(self, beacons: list[Beacon], distances: set[Distance]) -> None:
        self.beacons = beacons
        self.distances = distances


class Scanner:
    def __init__(self, _id: int, beacons: list[Beacon]) -> None:
        self.id = _id
        distances = [
            d for d in [diff(r1, r2) for r1 in beacons for r2 in beacons]
            if sq_norm(d) < CLOSE_NEIGH_CUTOFF_SQUARED
        ]
        self.data_orientations = [
            ScanData(
                {orn(*b) for b in beacons},
                {orn(*d) for d in distances},
            )
            for orn in orientations()
        ]


class CalibratedScanner:
    def __init__(
        self, _id: int, position: Position, beacons: set[Beacon], distances: set[int]
    ) -> None:
        self.id = _id
        self.position = position
        self.beacons = beacons
        self.distances = distances


def scanner_sees_beacon(scanner_position: Position, beacon_position: Position):
    return max(map(abs, diff(scanner_position, beacon_position))) <= MAX_DIST


def check_for_overlap(
    cs: CalibratedScanner, corrected_scanner_position: Position, offset_beacon_positions: Position
):
    new_beacons = set()
    match_count = 0
    for offset_beacon in offset_beacon_positions:
        beacon = add(corrected_scanner_position, offset_beacon)
        if beacon not in cs.beacons and scanner_sees_beacon(cs.position, beacon):
            # The scanner should already have spotted it
            return None
        new_beacons.add(beacon)
        if beacon in cs.beacons:
            match_count += 1
    if match_count < OVERLAP_THRESHOLD:
        return None
    return new_beacons


def attempt_oriented_calibration(
    cs: CalibratedScanner, uncalibrated_beacons: set[Beacon]
) -> None | tuple[Position, set[Beacon]]:
    for referance_beacon in uncalibrated_beacons:
        already_attempted = []
        for test in cs.beacons:
            new_scanner_position = diff(test, referance_beacon)
            if any(
                scanner_sees_beacon(new_scanner_position, aa)
                and diff(aa, new_scanner_position) not in uncalibrated_beacons
                for aa in already_attempted
            ):
                continue
            already_attempted.append(test)

            if new_beacon_positions := check_for_overlap(
                cs, new_scanner_position, uncalibrated_beacons
            ):
                return new_scanner_position, new_beacon_positions


def attempt_calibration(
    cs: CalibratedScanner, s: Scanner
) -> None | tuple[Position, set[Beacon], set[int]]:
    for data in s.data_orientations:
        distance_match = len(data.distances & cs.distances)
        if distance_match < CLOSE_DISTANCE_MATCH_THRESHOLD:
            continue
        if match := attempt_oriented_calibration(cs, data.beacons):
            position, beacons = match
            return position, beacons, data.distances


def calibrate_scanners(scanners: list[Scanner]):
    calibrated_scanners = {}

    # Define first scanner as reference frame
    start_id = 0
    start_pos = (0, 0, 0)
    start_data = scanners[start_id].data_orientations[0]
    calibrated_scanners[start_id] = CalibratedScanner(
        start_id, start_pos, start_data.beacons, start_data.distances
    )

    # Calibrate other scanners against it
    already_compared_scanner_pairs = set()
    while len(calibrated_scanners) < len(scanners):
        # Turn values to list, because the dict might change during iteration
        for cs in list(calibrated_scanners.values()):
            for s in scanners:
                if s.id in calibrated_scanners:
                    continue
                if cs.id == s.id:
                    continue
                if (cs.id, s.id) in already_compared_scanner_pairs:
                    continue
                already_compared_scanner_pairs |= {(cs.id, s.id), (s.id, cs.id)}

                if match := attempt_calibration(cs, s):
                    position, beacons, distances = match
                    calibrated_scanners[s.id] = CalibratedScanner(
                        s.id, position, beacons, distances
                    )
    return calibrated_scanners.values()


def get_readings_from_input_file() -> list[list[Beacon]]:
    with open("inputs/19", "r") as f:
        input_text = f.read().strip()

    # Remove headers
    headers = input_text.split("---")[1::2]
    assert all(header.startswith(" scanner ") for header in headers)
    scanner_outputs = input_text.split("---")[0::2]
    return [
        [tuple(map(int, line.split(","))) for line in output.strip().split("\n") if line]
        for output in scanner_outputs if output
    ]


def solve():
    scanners = [
        Scanner(i, beacons) for i, beacons in enumerate(get_readings_from_input_file())
    ]
    calibrated_scanners = calibrate_scanners(scanners)

    beacon_positions = {b for s in calibrated_scanners for b in s.beacons}
    yield len(beacon_positions)

    scanner_positions = [s.position for s in calibrated_scanners]
    metro_metric = max(
        sum(abs(e1 - e2) for e1, e2 in zip(r1,r2))
        for r1 in scanner_positions
        for r2 in scanner_positions
    )
    yield metro_metric


def solutions():
    yield 425
    yield 13354


if __name__ == "__main__":
    from helpers import main_template

    main_template(solve, solutions, with_timer=True)
