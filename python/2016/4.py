"""Security Through Obscurity"""
from typing import Iterator


def rotate(character: str, sector_id: int) -> str:
    return chr(ord("a") + (ord(character) - ord("a") + sector_id) % 26)


def decrypt(name: str, sector_id: int) -> str:
    return "".join(rotate(c, sector_id) if "a" <= c <= "z" else " " for c in name)


assert decrypt("qzmt-zixmtkozy-ivhz", 343) == "very encrypted name"


def parse(text: str) -> list[tuple[str, int, str]]:
    rooms = [
        line.replace("-", " ").replace("]", "").replace("[", " ").split()
        for line in text.splitlines()
    ]
    return [
        ("-".join(rest), int(sector_id), checksum)
        for *rest, sector_id, checksum in rooms
    ]


def is_real(name: str, checksum: str) -> bool:
    counts = {char: 0 for char in set(name)}
    for char in name:
        counts[char] += 1
    del counts["-"]

    grouped = {count: [] for count in set(counts.values())}
    for char, count in counts.items():
        grouped[count].append(char)

    calculated_checksum = "".join(
        "".join(sorted(grouped[count]))
        for count in sorted(grouped, reverse=True)
    )[:5]

    return calculated_checksum == checksum


def solve(text: str) -> Iterator:
    room_names = parse(text)

    real_rooms = [(name, sid, chx) for name, sid, chx in room_names if is_real(name, chx)]
    yield sum(sector_id for _, sector_id, _ in real_rooms)

    goal_name = "northpole object storage"
    yield next(sid for name, sid, _ in real_rooms if decrypt(name, sid) == goal_name)
