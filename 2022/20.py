def mix(positions):
    N = len(positions)
    for i in range(N):
        number, prev = positions[i]
        curr = (prev + number - 1) % (N - 1) + 1
        positions = [
            (n, other - (prev < other <= curr) + (curr <= other < prev))
            for n, other in positions
        ]
        positions[i] = (number, curr)
    return positions


def find_coordinates(positions):
    N = len(positions)
    zero_pos = next(pos for n, pos in positions if n == 0)
    return [n for n, pos in positions if (pos - zero_pos) % N in [1000, 2000, 3000]]


def solve(text):
    numbers = [int(line) for line in text.splitlines()]

    positions = [(number, i) for i, number in enumerate(numbers)]
    yield sum(find_coordinates(mix(positions)))

    positions = [(number * 811589153, i) for i, number in enumerate(numbers)]
    for i in range(10):
        positions = mix(positions)
    yield sum(find_coordinates(positions))


if __name__ == "__main__":
    from helpers import main_template

    main_template("20", solve)
