"""Camel Cards"""
from collections import Counter
from collections.abc import Iterator


"""Represent hand type by card frequencies: (5,), (4, 1), (3, 2), ..."""
HandType = tuple[int, ...]
Play = tuple[str, int]

card_repr = str.maketrans("TJQKA", "ABCDE")
JACK = "J".translate(card_repr)
JOKER = "1"
EMPTY = "0"


def parse(text: str) -> list[Play]:
    lines = map(str.split, text.strip().splitlines())
    return [(hand.translate(card_repr), int(bid)) for hand, bid in lines]


def get_hand_type(hand: str) -> HandType:
    if JOKER in hand:
        joker_values = (set(hand) - {JOKER}) or {EMPTY}
        return max(get_hand_type(hand.replace(JOKER, card)) for card in joker_values)
    return tuple(sorted(Counter(hand).values(), reverse=True))


def compute_winnings(hands: list[Play]) -> int:
    type_hand_bid_list = [(get_hand_type(hand), hand, bid) for hand, bid in hands]
    bids = [bid for _, _, bid in sorted(type_hand_bid_list)]
    return sum(rank * bid for rank, bid in enumerate(bids, start=1))


def solve(text: str) -> Iterator[int]:
    hands1 = parse(text)
    yield compute_winnings(hands1)
    hands2 = [(hand.replace(JACK, JOKER), bid) for hand, bid in hands1]
    yield compute_winnings(hands2)
