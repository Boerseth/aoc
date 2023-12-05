"""If You Give A Seed A Fertilizer"""
from collections.abc import Iterator


def joined(intervals: list[tuple[int, int]]) -> list[tuple[int, int]]:
    new_intervals = [intervals[0]]
    for start, end in intervals[1:]:
        previous_start, previous_end = new_intervals.pop()
        if start <= previous_end:
            new_intervals.append((previous_start, end))
        else:
            new_intervals.append((previous_start, previous_end))
            new_intervals.append((start, end))
    return new_intervals


class Ranges:
    def __init__(self, intervals: list[tuple[int, int]]) -> None:
        self.intervals = [i for i in intervals]
        self._validate()

    def _validate(self) -> None:
        assert all(
            end1 < start2 for (_, end1), (start2, _) in zip(self.intervals, self.intervals[1:])
        )

    def split(self, splitting_starts: list[int]) -> None:
        new_intervals = []
        for start, end in self.intervals:
            # Can be optimized, since everything is sorted
            starts = [s for s in splitting_starts if start < s <= end]
            new_intervals += [(s, e - 1) for s, e in zip([start] + starts, starts + [end])]
        self.intervals = new_intervals
        self._validate()

    def lower_bound(self) -> int:
        self._validate()
        return self.intervals[0][0]


class Map:
    def __init__(self, maps: list[tuple[int, int, int]]) -> None:
        """
        The dict _map defines starting points for transformation rules
        so that
            _map[start1] == target1
            _map[start1 + i] == target1 + i  and  i < start2 - start1
        """
        self._map = {}
        for target_start, source_start, length in maps:
            self._map[source_start] = target_start
            # Fill in gaps by maybe also setting after-interval to identity
            next_source_start = source_start + length
            if next_source_start not in self._map:
                self._map[next_source_start] = next_source_start
        self.interval_starts = sorted(self._map)

    def get_start_of_interval(self, value: int) -> int | None:
        # Can be optimized using binary search
        return max((s for s in self.interval_starts if s <= value), default=None)

    def apply(self, source: int) -> int:
        start = self.get_start_of_interval(source)
        if start is None:
            return source
        return self._map[start] + source - start

    def apply_to_ranges(self, ranges: Ranges) -> Ranges:
        ranges.split(self.interval_starts)
        new_intervals = [(self.apply(start), self.apply(end)) for start, end in ranges.intervals]
        return Ranges(joined(sorted(new_intervals)))


def parse(text: str) -> None:
    seed_line, *map_texts = text.strip().split("\n\n")
    seeds = [int(seed) for seed in seed_line.split()[1:]]
    maps = [[map(int, r.split()) for r in map_text.splitlines()[1:]] for map_text in map_texts]
    return seeds, maps


def solve(text: str) -> Iterator[int]:
    seeds, raw_maps = parse(text)
    maps = [Map(raw_map) for raw_map in raw_maps]

    values = [s for s in seeds]
    for m in maps:
        values = [m.apply(val) for val in values]
    yield min(values)

    ranges = Ranges(sorted((s, s + l - 1) for s, l in zip(seeds[::2], seeds[1::2])))
    for m in maps:
        ranges = m.apply_to_ranges(ranges)
    yield ranges.lower_bound()
