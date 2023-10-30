"""The Ideal Stocking Stuffer"""
import hashlib
from typing import Iterator


def miner(seed: str, goal: str) -> int:
    nonce = 0
    while not hashlib.md5(f"{seed}{nonce}".encode()).hexdigest().startswith(goal):
        nonce += 1
    return nonce


def solve(text: str) -> Iterator[int]:
    text = text.strip()
    yield miner(text, "00000")
    yield miner(text, "000000")
