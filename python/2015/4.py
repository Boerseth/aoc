import hashlib


def miner(seed, n):
    nonce = 0
    while not hashlib.md5((seed + str(nonce)).encode()).hexdigest().encode().startswith(b"0" * n):
        nonce += 1
    return nonce


def solve():
    with open("inputs/4", "r") as f:
        text = f.readline().strip()
    yield miner(text, 5)
    yield miner(text, 6)


def solutions():
    yield 346386
    yield 9958218


if __name__ == "__main__":
    from helpers import main_template

    main_template(solve, solutions)
