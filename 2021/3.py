def filter_data_bitwise(filtered_data, filter_bit, filter_by_most_common=True):
    if len(filtered_data) == 1 or filter_bit == 0:
        return filtered_data
    ratio = sum(1 for num in filtered_data if num & filter_bit) / len(filtered_data)
    wanted_bit_value = filter_bit * int((ratio >= 0.5) == filter_by_most_common)
    return filter_data_bitwise(
        [x for x in filtered_data if x & filter_bit == wanted_bit_value],
        filter_bit >> 1,
        filter_by_most_common,
    )


def solve():
    lines = [line for line in open("inputs/3", "r").readlines()]
    N = len(lines[0].strip())  # number of bits in each number
    data = [int(line, base=2) for line in lines]


    bits = [2 ** n for n in range(N)]
    gamma = sum(bit for bit in bits if sum(datum & bit for datum in data) // bit >= len(data) / 2)
    epsilon = sum(bit for bit in bits if sum(datum & bit for datum in data) // bit <= len(data) / 2)
    yield epsilon * gamma

    filtered_by_most_common = filter_data_bitwise(data, 2 ** (N - 1))
    filtered_by_least_common = filter_data_bitwise(data, 2 ** (N - 1), filter_by_most_common=False)
    yield filtered_by_most_common[0] * filtered_by_least_common[0]


def solutions():
    yield 3895776
    yield 7928162


if __name__ == "__main__":
    from helpers import main_template

    main_template(solve, solutions)
