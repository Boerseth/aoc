"""Explosives in Cyberspace"""
from typing import Iterator


def find_length_2(compressed: str) -> int:
    paren_start = compressed.find("(")
    if paren_start == -1:
        return len(compressed)
    decompressed_length = paren_start

    while paren_start >= 0:
        paren_end = compressed.find(")", paren_start)
        assert paren_end >= 0, compressed
        length, mult = compressed[paren_start + 1 : paren_end].split("x")

        chunk_start = paren_end + 1
        chunk_end = chunk_start + int(length)
        decompressed_length += int(mult) * find_length_2(compressed[chunk_start:chunk_end])

        paren_start = compressed.find("(", chunk_end)
        decompressed_length += len(compressed[chunk_end:paren_start])
    decompressed_length += len(compressed) - chunk_end
    return decompressed_length


def find_length_1(compressed: str) -> int:
    decompressed_length = 0
    paren_start = compressed.find("(")
    if paren_start == -1:
        return len(compressed)

    while paren_start >= 0:
        paren_end = compressed.find(")", paren_start)
        assert paren_end >= paren_start + 3, (paren_start, paren_end)
        length, mult = compressed[paren_start + 1 : paren_end].split("x")

        chunk_start = paren_end + 1
        chunk_end = chunk_start + int(length)
        decompressed_length += int(length) * int(mult)

        paren_start = compressed.find("(", chunk_end)
    return decompressed_length


def there_are_nested_or_unmatched_parens(compressed: str) -> bool:
    i = 0
    for char in compressed:
        if char == "(":
            i += 1
        if char == ")":
            i -= 1
        if i not in [0, 1]:
            return True
    return i != 0


def ignore_whitespace(text: str) -> str:
    return "".join(text.strip().split())


def solve(text: str) -> Iterator:
    compressed = ignore_whitespace(text)
    assert not there_are_nested_parens(compressed)
    yield find_length_1(compressed)
    yield find_length_2(compressed)
