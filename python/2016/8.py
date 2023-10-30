"""Two-Factor Authentication"""
from typing import Iterator


Screen = list[list[bool]]
WIDTH = 50
HEIGHT = 6
Cs = list(range(WIDTH))
Rs = list(range(HEIGHT))


def rect(screen: Screen, width: int, height: int) -> Screen:
    return [[screen[r][c] or (r < height and c < width) for c in Cs] for r in Rs]


def rotate_row(screen: Screen, row: int, n: int) -> Screen:
    return [[screen[r][c if r != row else (c - n) % WIDTH] for c in Cs] for r in Rs]


def rotate_col(screen: Screen, col: int, n: int) -> Screen:
    return [[screen[r if c != col else (r - n) % HEIGHT][c] for c in Cs] for r in Rs]


def do_operation(screen: Screen, operation: list[str]) -> Screen:
    match operation:
        case "rect", width, "x", height:
            return rect(screen, int(width), int(height))
        case "rotate", "row", "y", "=", row, "by", n:
            return rotate_row(screen, int(row), int(n))
        case "rotate", "column", "x", "=", col, "by", n:
            return rotate_col(screen, int(col), int(n))


def get_screen_output(screen: Screen) -> None:
    return "".join("\n" + "".join(" #"[pix] for pix in row) for row in screen)


def parse(text: str) -> list:
    for line in text.strip().splitlines():
        yield line.replace("x", " x ").replace("=", " = ").split()


def solve(text: str) -> Iterator[int | str]:
    screen = [[False for _ in range(WIDTH)] for _ in range(HEIGHT)]
    for operation in parse(text):
        screen = do_operation(screen, operation)

    yield sum(pix for row in screen for pix in row)
    yield get_screen_output(screen)
