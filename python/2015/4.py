"""The Ideal Stocking Stuffer"""

import hashlib


def miner(seed, n):
    nonce = 0
    while not hashlib.md5((seed + str(nonce)).encode()).hexdigest().encode().startswith(b"0" * n):
        nonce += 1
    return nonce


def solve(text):
    text = text.strip()
    yield miner(text, 5)
    yield miner(text, 6)
