"""Opening the Turing Lock"""
from typing import Callable, Iterator


Memory = tuple[int, int, int]
Instruction = Callable[[Memory], Memory]


def flip(register: str, instruction: Instruction) -> Callable[[str, Instruction], Instruction]:
    if register == "a":
        return instruction
    return lambda a, i, b: instruction(b, i, a)[::-1]


def get_function(*args) -> Instruction:
    match args:
        case "hlf", r:
            return flip(r, lambda a, i, b: (a // 2, i + 1, b))
        case "tpl", r:
            return flip(r, lambda a, i, b: (a * 3, i + 1, b))
        case "inc", r:
            return flip(r, lambda a, i, b: (a + 1, i + 1, b))

    *jump_args, offset = args
    off = int(offset)
    match jump_args:
        case "jmp",:
            return lambda a, i, b: (a, i + off, b)
        case "jie", r:
            return flip(r, lambda a, i, b: (a, i + 1 if a % 2 else i + off, b))
        case "jio", r:
            return flip(r, lambda a, i, b: (a, i + 1 if a != 1 else i + off, b))
    raise Exception()


def parse(text: str) -> list[Instruction]:
    lines = text.strip().replace(",", "").replace("+", "").splitlines()
    return [get_function(*line.split()) for line in lines]


def solve(text: str) -> Iterator[int]:
    instructions = parse(text)

    a = i = b = 0
    while 0 <= i < len(instructions):
        a, i, b = instructions[i](a, i, b)
    yield b

    i = b = 0
    a = 1
    while 0 <= i < len(instructions):
        a, i, b = instructions[i](a, i, b)
    yield b
