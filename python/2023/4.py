"""Scratchcards"""
from collections.abc import Iterator


def parse(text: str) -> list:
    lines = text.strip().splitlines()
    cards = {}
    for line in lines:
        # Card 123: 1 2 3 | 4 5 6 7 8
        card_id, wins, haves = line.replace("Card", "").replace(":", "|").split("|")
        cards[int(card_id)] = (list(map(int, wins.split())), list(map(int, haves.split())))
    return cards


def calculate_points(winning_numbers: list[int], had_numbers: list[int]) -> int:
    hits = set(winning_numbers) & set(had_numbers)
    return int(2 ** (len(hits) - 1))


def solve(text: str) -> Iterator[int]:
    scratchcards = parse(text)
    yield sum(calculate_points(*scratchcard) for scratchcard in scratchcards.values())

    card_copies = {card_id: 1 for card_id in scratchcards}
    for card_id in sorted(scratchcards):
        winning_numbers, had_numbers = scratchcards[card_id]
        hits = set(winning_numbers) & set(had_numbers)
        for copied_card_id in range(card_id + 1, card_id + 1 + len(hits)):
            card_copies[copied_card_id] += card_copies[card_id]
    yield sum(card_copies.values())

