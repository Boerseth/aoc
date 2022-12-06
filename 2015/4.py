import hashlib


puzzle = open("inputs/4", "r").readline().strip()


def miner(seed, n):
    nonce = 0
    while not hashlib.md5((seed + str(nonce)).encode()).hexdigest().encode().startswith(b"0" * n):
        nonce += 1
    return nonce


# Part 1
print("Part 1:", miner(puzzle, 5))



# Part 2
print("Part 2:", miner(puzzle, 6))
