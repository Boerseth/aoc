import argparse


def parse_args() -> tuple[int | None, int | None, bool, bool, bool]:
    parser = argparse.ArgumentParser(
        prog=f"python3 python/main.py",
        description=f"Solve a day of AoC using the Python solution (if available)",
        epilog="Good luck!",
    )
    parser.add_argument(
        "-y",
        "--year",
        type=int,
        default=None,
        required=False,
        help="Year from which to choose problem. If not provided, solve all years.",
    )
    parser.add_argument(
        "-d",
        "--day",
        type=int,
        default=None,
        required=False,
        help="Day to solve. If not provided, solve all days.",
    )
    parser.add_argument(
        "-n",
        "--no-assert",
        action="store_true",
        default=False,
        required=False,
        help="Do not assert that computed answer equals solution",
    )
    parser.add_argument(
        "-t",
        "--time-it",
        action="store_true",
        default=False,
        required=False,
        help="Print table of time taken for the two parts",
    )
    parser.add_argument(
        "--test",
        action="store_true",
        default=False,
        required=False,
        help="Run with test input",
    )

    args = parser.parse_args()
    return args.year, args.day, args.test, not args.no_assert, args.time_it
