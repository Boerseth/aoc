"""Reindeer Olympics"""
from typing import Iterator


class Reindeer:
    def __init__(self, name: str, speed: int, fly_time: int, rest_time: int) -> None:
        self.name = name
        self.speed = speed
        self.fly_time = fly_time
        self.rest_time = rest_time
        self.period = fly_time + rest_time

        self.position = 0
        self.remaining_fly_time = fly_time
        self.remaining_rest_time = 0
        self.points = 0

    def distance_after(self, time: int) -> int:
        distance = 0
        for sec in range(self.fly_time):
            # Each second every cycle
            for cycle in range(time // self.period):
                distance += self.speed
            # Only some of the seconds the last cycle
            if sec < time % self.period:
                distance += self.speed
        return distance

    def _fly(self) -> None:
        self.position += self.speed
        self.remaining_fly_time -= 1
        if not self.remaining_fly_time:
            self.remaining_rest_time = self.rest_time

    def _rest(self) -> None:
        self.remaining_rest_time -= 1
        if not self.remaining_rest_time:
            self.remaining_fly_time = self.fly_time

    def timestep(self) -> None:
        if self.remaining_fly_time:
            self._fly()
            return
        assert self.remaining_rest_time
        self._rest()


def parse(text: str) -> list[Reindeer]:
    reindeer = []
    for line in text.splitlines():
        (name, _, _, speed, _, _, fly_time, *_, rest_time, _) = line.split()
        reindeer.append(Reindeer(name, int(speed), int(fly_time), int(rest_time)))
    return reindeer


def solve(text) -> Iterator[int]:
    reindeer = parse(text)
    distances = [r.distance_after(2503) for r in reindeer]
    yield max(distances)

    for _ in range(1, 2503 + 1):
        for r in reindeer:
            r.timestep()
        furthest = max(r.position for r in reindeer)
        for r in reindeer:
            if r.position == furthest:
                r.points += 1
    yield max((r for r  in reindeer), key=lambda _r: _r.points).points
