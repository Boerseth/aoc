"""Haunted Wasteland"""
from collections.abc import Iterable, Iterator
from math import gcd, lcm
from typing import Literal


"""
In the end, we want the lowest solution `N` such that, for all `i`
    N = targets[i] + cycle_length[i] * n[i]
For some integer vectors `cycle_length[:]` and `n[:]`.

This is a set of linear Diophantine equations.

It is known that `N` must be a multiple of all `gcd(target, length)`, which
gives us a list of divisors.
"""

Instruction = Literal["L", "R"]
LEFT: Instruction = "L"
RIGHT: Instruction = "R"

Node = str
START: Node = "AAA"
GOAL: Node = "ZZZ"

Network = dict[Node, dict[Instruction, Node]]


def parse(text: str) -> None:
    instructions, _, *rest = text.strip().splitlines()
    remove_symbols = str.maketrans("=(,)", "    ")
    network = {}
    for line in rest:
        source, left, right = line.translate(remove_symbols).split()
        network[source] = {LEFT: left, RIGHT: right}
    return instructions, network


def loop(iterator: Iterable) -> Iterator:
    while True:
        for it in iterator:
            yield it


def get_steps_to_goal(network: Network, instructions: list[Instruction]) -> int:
    node = START
    for count, instruction in enumerate(loop(instructions), start=1):
        node = network[node][instruction]
        if node == GOAL:
            return count


def get_divisor(network: Network, instructions: list[Instruction], pos: Node) -> list[int]:
    history = {(pos, 0): 0}
    cycle_start = None
    cycle_end = None
    targets = []
    for count, instruction in enumerate(loop(instructions), start=1):
        pos = network[pos][instruction]
        mod = count % len(instructions)
        if (pos, mod) in history:
            cycle_start = history[pos, mod]
            cycle_end = count
            break
        if pos.endswith("Z"):
            targets.append(count)
        history[pos, mod] = count
    assert len(targets) == 1, "This just happens to be the case for the dataset"
    target = targets.pop()
    length = cycle_end - cycle_start
    return gcd(target, length)


def solve(text: str) -> Iterator:
    instructions, network = parse(text)
    yield get_steps_to_goal(network, instructions)
    starts = [pos for pos in network if pos.endswith("A")]
    divisors = [get_divisor(network, instructions, pos) for pos in starts]
    yield lcm(*divisors)
