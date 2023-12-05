"""Scratchcards"""
from collections.abc import Iterator


def parse(text: str) -> list:
    lines = text.strip().splitlines()
    cards = []
    for line in lines:
        _, card_id, *rest = line.split()
        divider = rest.index("|")
        win_nums = rest[:divider]
        have_nums = rest[divider + 1 :]
        cards.append((int(card_id[:-1]), list(map(int, win_nums)), list(map(int, have_nums))))
    return cards


def _parse(text: str) -> list:
    lines = text.strip().splitlines()
    scratchcards = []
    for line in lines:
        card_identifier, numbers = line.split(": ")
        card_id = card_identifier.split()[1]
        winning_numbers, had_numbers = [nums.strip().split() for nums in numbers.split("|")]
        scratchcards.append(
            (int(card_id), list(map(int, winning_numbers)), list(map(int, had_numbers)))
        )
    return scratchcards


def calculate_points(card_id: int, winning_numbers: list[int], had_numbers: list[int]) -> int:
    hits = set(winning_numbers) & set(had_numbers)
    return int(2 ** (len(hits) - 1))



def solve(text: str) -> Iterator[int]:
    scratchcards = parse(text)
    yield sum(calculate_points(*scratchcard) for scratchcard in scratchcards)

    card_copies = {card_number: 1 for card_number, *_ in scratchcards}
    for card_id, winning_numbers, had_numbers in scratchcards:
        hits = set(winning_numbers) & set(had_numbers)
        for copied_card_id in range(card_id + 1, card_id + 1 + len(hits)):
            card_copies[copied_card_id] += card_copies[card_id]
    yield sum(card_copies.values())

