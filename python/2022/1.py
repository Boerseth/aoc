"""Calorie Counting"""


def get_top_n(numbers, n):
    top_group = numbers[:1]
    for number in numbers[1:]:
        i = 0
        while any(top < number for top in top_group[i:]):
            i += 1
        top_group = (top_group[:i] + [number] + top_group[i:])[-n:]
    return top_group


def solve(text):
    elf_inventory_lists = [
        [int(line) for line in chunk.splitlines()] for chunk in text.split("\n\n")
    ]
    totals = [sum(inv) for inv in elf_inventory_lists]

    # sorted_totals = sorted(totals)
    # yield sorted_totals[-1]
    # yield sum(sorted_totals[-3:])
    yield sum(get_top_n(totals, 1))
    yield sum(get_top_n(totals, 3))
