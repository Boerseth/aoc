#!/usr/bin/env python3
from importlib import import_module, util
from os import path, walk

from tools.arguments import parse_args
from tools.problem import Problem
from tools.timer import Timer


SCRIPT_LOCATION = path.realpath(__file__)
ROOT = SCRIPT_LOCATION.split("/python/")[0]
PROBLEMS_DIR = f"{ROOT}/aoc-problems"


def _get_all_years():
    return sorted(list(map(int, next(walk(PROBLEMS_DIR))[1])))


def _get_all_days(year: int):
    return sorted(list(map(int, next(walk(f"{PROBLEMS_DIR}/{year}"))[1])))


def solve(
    year: int,
    day: int,
    with_test: bool,
    with_assert: bool,
    with_timer: bool,
) -> None:
    module = import_module(f"{year}.{day}")
    title = f"AoC - Year {year}, Day {day}: {module.__doc__}"

    timer = Timer(title)
    problem = Problem(year, day, with_test, PROBLEMS_DIR)

    problem_solutions = problem.solutions()
    answers = module.solve(problem.input())  # Won't start until next() is called

    print(title)
    for part, solution in zip([1, 2], problem_solutions):
        part_title = f"  Part {part}:"

        with timer.time_block(part_title):
            try:
                answer = next(answers)
            except StopIteration:
                answer = None
        print(part_title, answer)

        if with_assert:
            assert answer == solution, f"\n\n{answer}\n =!= \n{solution}\n"

    if with_timer:
        timer.print_table()


def main(
    year: int | None,
    day: int | None,
    with_test: bool,
    with_assert: bool,
    with_timer: bool,
) -> None:
    years = [year] if year is not None else _get_all_years()
    for year in years:
        if not util.find_spec(f"{year}"):
            continue
        days = [day] if day is not None else _get_all_days(year)
        for day in days:
            if not util.find_spec(f"{year}.{day}"):
                continue
            solve(year, day, with_test, with_assert, with_timer)


if __name__ == "__main__":
    main(*parse_args())
