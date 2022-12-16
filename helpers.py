import argparse
import json
from contextlib import contextmanager
from time import time
from typing import Any, Callable, Iterator, TypeVar
from sys import argv

T = TypeVar("T")


def _read_from_file(path: str) -> str:
    with open(path, "r") as f:
        return f.read()


def _parse_args(day: str) -> tuple[str, list[int | str], bool, bool]:
    default_input_path = f"inputs/{day}"
    default_solution_path = f"solutions/{day}.json"

    parser = argparse.ArgumentParser(
        prog=f"python3 {day}.py",
        description=f"Solves the problems 1 and 2 from Advent of Code, day {day}",
        epilog="Good luck!",
    )
    parser.add_argument(
        "--input",
        default=default_input_path,
        required=False,
        help=f"Path to problem input",
        type=str,
    )
    parser.add_argument(
        "--solution",
        default=default_solution_path,
        required=False,
        help=f"Path to json-formatted problem solutions",
        type=str,
    )
    parser.add_argument(
        "--timer",
        action="store_true",
        default=False,
        required=False,
        help="Print table of time taken for the two parts",
    )
    parser.add_argument(
        "--no-assert",
        action="store_true",
        default=False,
        required=False,
        help="Do not assert that computed answer equals solution",
    )

    args = parser.parse_args()
    problem_input = _read_from_file(args.input)
    solutions_json = _read_from_file(args.solution) if not args.no_assert else "[null, null]"
    solutions = json.loads(solutions_json)

    return problem_input, solutions, not args.no_assert, args.timer


def main_template(day: str, solve: Callable[[str], Iterator[int | str]]) -> None:
    problem_input, solutions, with_assert, with_timer = _parse_args(day)

    timer = Timer(f"Day {day}")
    kwargs = {"timer": timer} if solve.__code__.co_argcount >= 2 else {}
    solver = solve(problem_input, **kwargs)

    for part, expectation in zip([1, 2], solutions):
        with timer.time_block(f"Part {part}"):
            result = next(solver)
        print(f"Part {part}:", result)
        if with_assert:
            assert result == expectation, (result, expectation)

    if with_timer:
        timer.print_table()


def _get_table_row(key: str, key_width: int, total: float, val: float) -> str:
    row_name = key.ljust(key_width)
    percentage = str(int(100 * val / total)).rjust(5) + "%"
    return f"{row_name} {percentage} - {val}"


class Timer:
    def __init__(self, title: str) -> None:
        self.title = title
        self.block_bins = {}
        self.function_bins = {}

    @contextmanager
    def time_block(self, key: str) -> Iterator:
        if key not in self.block_bins:
            self.block_bins[key] = 0
        start = time()
        yield
        self.block_bins[key] += time() - start

    def time_function(self, f: Callable[..., T]) -> Callable[..., T]:
        key = f.__name__
        if key in self.function_bins:
            n = sum(1 for k in self.function_bins if k.startswith(key))
            key += f":{n + 1}"
        self.function_bins[key] = 0

        def wrapper(*args: Any, **kwargs: Any) -> T:
            start = time()
            result = f(*args, **kwargs)
            self.function_bins[key] += time() - start
            return result

        return wrapper

    def print_results(self) -> None:
        if self.block_bins:
            print("Blocks:")
            for key, val in self.block_bins.items():
                print(key, val)
        if self.function_bins:
            print("Functions:")
            for key, val in self.funciton_bins.items():
                print(key, val)
        if not (self.block_bins or self.function_bins):
            print("No timer results")

    def print_table(self) -> None:
        if not (self.block_bins or self.function_bins):
            print("No timer results")
            return

        max_block_key_width = len(max(self.block_bins.keys() or [""], key=len))
        max_function_key_width = len(max(self.function_bins.keys() or [""], key=len))
        key_width = max(max_block_key_width, max_function_key_width)

        block_total = sum(self.block_bins.values())
        function_total = sum(self.function_bins.values())
        block_rows = [
            _get_table_row(key, key_width, block_total, val)
            for key, val in self.block_bins.items()
            if block_total
        ]
        function_rows = [
            _get_table_row(key, key_width, function_total, val)
            for key, val in self.function_bins.items()
            if function_total
        ]
        cols = len(max(block_rows + function_rows, key=len))

        print("\n" + self.title.center(cols))
        if block_rows:
            print("-" * cols + "\nBlocks: " + str(block_total))
            for row in block_rows:
                print(row)

        if function_rows:
            print("-" * cols + "\nFunctions: " + str(function_total))
            for row in function_rows:
                print(row)
        print("-" * cols)
