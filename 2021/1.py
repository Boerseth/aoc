def solve():
    depths = [int(line) for line in open("input_1", "r").readlines()]
    yield sum(1 for d1, d2 in zip(depths, depths[1:]) if d1 < d2)
    yield sum(1 for d1, d2 in zip(depths, depths[3:]) if d1 < d2)


def solutions():
    yield 1215
    yield 1150


def main():
    for part, result, solution in zip([1, 2], solve(), solutions()):
        print(f"Part {part}:", result)
        assert result == solution


if __name__ == "__main__":
    main()
