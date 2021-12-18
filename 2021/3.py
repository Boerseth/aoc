with open("input_3", "r") as f:
    lines = f.readlines()

N = len(lines[0].strip())  # number of bits in each number
data = [int(line, base=2) for line in lines]


# Part 1
bits = [2 ** n for n in range(N)]
gamma = sum(bit for bit in bits if sum(datum & bit for datum in data) // bit >= len(data) / 2)
epsilon = sum(bit for bit in bits if sum(datum & bit for datum in data) // bit <= len(data) / 2)
print(epsilon * gamma)


# Part 2
def filter_data_bitwise(data, filter_by_most_common=True):
    filtered = [x for x in data]
    for bit in reversed(bits):
        ratio = sum(1 for num in filtered if num & bit) / len(filtered)
        wanted_bit_value = bit * int((ratio >= 0.5) == filter_by_most_common)
        filtered = [x for x in filtered if x & bit == wanted_bit_value]
        if len(filtered) == 1:
            break
    return filtered

def filter_data_bitwise_r(filtered_data, filter_bits, filter_by_most_common=True):
    if len(filtered_data) == 1 or not filter_bits:
        return filtered_data
    bit = filter_bits[0]
    ratio = sum(1 for num in filtered_data if num & bit) / len(filtered_data)
    wanted_bit_value = bit * int((ratio >= 0.5) == filter_by_most_common)
    return filter_data_bitwise_r(
        [x for x in filtered_data if x & bit == wanted_bit_value],
        filter_bits[1:],
        filter_by_most_common,
    )
    

filtered_by_most_common = filter_data_bitwise(data)
filtered_by_least_common = filter_data_bitwise(data, filter_by_most_common=False)
print(filtered_by_most_common[0] * filtered_by_least_common[0])
filtered_by_most_common = filter_data_bitwise_r(data, list(reversed(bits)))
filtered_by_least_common = filter_data_bitwise_r(data, list(reversed(bits)), filter_by_most_common=False)
print(filtered_by_most_common[0] * filtered_by_least_common[0])
