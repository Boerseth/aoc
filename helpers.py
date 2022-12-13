import json
from contextlib import contextmanager
from time import time
from sys import argv


def load_solutions(N, with_assert):
    if with_assert:
        with open(f"solutions/{N}.json", "r") as f:
            solutions = json.loads(f.read())
        return solutions
    else:
        return [None, None]



def main_template(
    N, solve, solutions=None, with_assert=True, with_timer=False
):
    if not solutions:
        solutions = load_solutions(N, with_assert)
    with open(f"inputs/{N}", "r") as f:
        problem_input = f.read()

    solver = solve(problem_input)

    timer = Timer(f"Day {N}")
    for part, expectation in zip([1, 2], solutions):
        with timer.time_block(f"Part {part}"):
            result = next(solver)
        print(f"Part {part}:", result)
        if with_assert:
            assert result == expectation, (result, expectation)

    if with_timer:
        timer.print_table()


def _get_table_row(key, key_width, total, val):
    row_name = key.ljust(key_width)
    percentage = str(int(100 * val / total)).rjust(5) + "%"
    return f"{row_name} {percentage} - {val}"


class Timer:
    def __init__(self, title):

        self.title = title
        self.block_bins = {}
        self.function_bins = {}

    @contextmanager
    def time_block(self, key):
        if key not in self.block_bins:
            self.block_bins[key] = 0
        start = time()
        yield
        self.block_bins[key] += time() - start

    def time_function(self, f):
        key = f.__name__
        if key in self.function_bins:
            n = sum(1 for k in self.function_bins if k.startswith(key))
            key += f":{n + 1}"
        self.function_bins[key] = 0

        def wrapper(*args, **kwargs):
            start = time()
            result = f(*args, **kwargs)
            self.function_bins[key] += time() - start
            return result

        return wrapper

    def print_results(self):
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

    def print_table(self):
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
