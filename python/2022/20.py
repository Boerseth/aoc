"""Grove Positioning System"""


def mix(numbers, indices):
    N = len(numbers)
    for i, number in enumerate(numbers):
        prev = indices.index(i)
        curr = (prev + number - 1) % (N - 1) + 1
        indices.pop(prev)
        indices.insert(curr, i)
    return indices


def find_coordinates(numbers, indices):
    N = len(numbers)
    zero_pos = indices.index(numbers.index(0))
    coordinate_indices = [indices[(zero_pos + i) % N] for i in [1000, 2000, 3000]]
    return [numbers[i] for i in coordinate_indices]


def solve(text):
    numbers = [int(line) for line in text.splitlines()]
    indices = list(range(len(numbers)))
    yield sum(find_coordinates(numbers, mix(numbers, indices)))

    numbers = [n * 811589153 for n in numbers]
    indices = list(range(len(numbers)))
    for _ in range(10):
        indices = mix(numbers, indices)
    yield sum(find_coordinates(numbers, indices))
