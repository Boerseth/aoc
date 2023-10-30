"""Internet Protocol Version 7"""
import re
from typing import Callable, Iterator


def collect(seq: str, find_match: Callable) -> Iterator[str]:
    for i in range(len(seq)):
        if match := find_match(seq[i:]):
            yield match


def maybe_abba(word: str) -> bool:
    a, b, c, d, *_ = word + "=" * max(0, 4 - len(word))
    return a == d and b == c and a != b and f"{a}{b}{c}{d}"


def supports_tls(supers: list[str], hypers: list[str]) -> bool:
    if any(abba for seq in hypers for abba in collect(seq, maybe_abba)):
        return False
    return any(abba for seq in supers for abba in collect(seq, maybe_abba))


def maybe_aba(word: str) -> bool:
    a, b, c, *_ = word + "=" * max(0, 3 - len(word))
    return a == c and a != b and f"{a}{b}{c}"


def supports_ssl(supers: list[str], hypers: list[str]) -> bool:
    abas = [aba for seq in supers for aba in collect(seq, maybe_aba)]
    babs = (bab for seq in hypers for bab in collect(seq, maybe_aba))
    return any(aba[1:] == bab[:2] for bab in babs for aba in abas)


def parse(ip: str) -> tuple[list[str], list[str]]:
    parts = ip.replace("[", " [ ").replace("]", " ] ").split()
    assert all(part == "[" for part in parts[1::4])
    assert all(part == "]" for part in parts[3::4])
    return parts[::4], parts[2::4]


def solve(text: str) -> Iterator:
    sequences = [parse(ip) for ip in text.strip().splitlines()]
    yield sum(supports_tls(supers, hypers) for supers, hypers in sequences)
    yield sum(supports_ssl(supers, hypers) for supers, hypers in sequences)
