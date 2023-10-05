"""The Ideal Stocking Stuffer"""

import hashlib


def miner(seed, goal):
    nonce = 0
    while not hashlib.md5(f"{seed}{nonce}".encode()).hexdigest().startswith(goal):
        nonce += 1
    return nonce


def solve(text):
    text = text.strip()
    yield miner(text, "00000")
    yield miner(text, "000000")
