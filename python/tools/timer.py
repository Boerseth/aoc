from contextlib import contextmanager
from time import time
from typing import Any, Callable, Iterator, TypeVar


T = TypeVar("T")


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
