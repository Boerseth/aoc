# because "AAA".count("AA") == 1 ...
def properly_count_substring(string, substring):
    return sum(1 for i in range(len(string)) if string[i:].startswith(substring))


def generate_element_count(freqs, pair_sources, N):
    for _ in range(N):
        freqs = {p: sum(freqs[source] for source in pair_sources[p]) for p in freqs}
    count = {element: 0 for pair in freqs for element in pair}
    for pair, freq in freqs.items():
        count[pair[0]] += freq
        count[pair[1]] += freq
    # All elements have been counted in pairs, EXCEPT for the first and last in the template
    return [(value + 1) // 2 for value in count.values()]


def solve(text):
    data = [line.strip() for line in text.splitlines() if line.strip()]
    polymer_template = data.pop(0)
    insertion_rule = dict(d.split(" -> ") for d in data)

    frequencies = {pair: properly_count_substring(polymer_template, pair) for pair in insertion_rule}
    pair_sources = {pair: [] for pair in insertion_rule}
    for source, insert in insertion_rule.items():
        pair_sources[source[0] + insert].append(source)
        pair_sources[insert + source[1]].append(source)

    part_1_count = generate_element_count(frequencies, pair_sources, 10)
    yield max(part_1_count) - min(part_1_count)
    part_2_count = generate_element_count(frequencies, pair_sources, 40)
    yield max(part_2_count) - min(part_2_count)
