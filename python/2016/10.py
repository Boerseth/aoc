"""Balance Bots"""
from typing import Iterator


def parse(text: str) -> tuple[list[tuple[int, str]], dict[str, dict[str, str | int]]]:
    givings = []
    destinations = {}
    for instruction in text.strip().splitlines():
        match instruction.split():
            case "value", val, *_, dest, bot:
                givings.append((int(val), f"{dest}_{bot}"))
            case dest, giver, _, _, _, dest_low, out_low, _, _, _, dest_high, out_high:
                destinations[f"{dest}_{giver}"] = {
                    "low": f"{dest_low}_{out_low}",
                    "high": f"{dest_high}_{out_high}",
                }
    return givings, destinations


def give(destinations: dict[str, dict[str, str | int]], val: int, dest: str) -> None:
    if dest not in destinations:
        destinations[dest] = {}
    if "has" not in destinations[dest]:
        destinations[dest]["has"] = val
        return

    other_val = destinations[dest]["has"]
    destinations[dest]["had"] = {val, other_val}
    give(destinations, min(val, other_val), destinations[dest]["low"])
    give(destinations, max(val, other_val), destinations[dest]["high"])


def solve(text: str) -> Iterator:
    givings, destinations = parse(text)
    for val, dest in givings:
        give(destinations, val, dest)
    for bot_name, info in destinations.items():
        if info.get("had") == {17, 61}:
            yield int(bot_name.split("_")[1])

    product = 1
    for i in range(3):
        product *= destinations[f"output_{i}"]["has"]
    yield product
