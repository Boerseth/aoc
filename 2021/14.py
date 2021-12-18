data = [line.strip() for line in open("input_14", "r").readlines() if line.strip()]
polymer_template = data.pop(0)
insertion_rule = dict(d.split(" -> ") for d in data)


# because "AAA".count("AA") == 1 ...
def properly_count_substring(string, substring):
    return sum(1 for i in range(len(string)) if string[i:].startswith(substring))


frequencies = {pair: properly_count_substring(polymer_template, pair) for pair in insertion_rule}
pair_sources = {pair: [] for pair in insertion_rule}
for source, insert in insertion_rule.items():
    pair_sources[source[0] + insert].append(source)
    pair_sources[insert + source[1]].append(source)


def generate_element_count(freqs, N):
    for _ in range(N):
        freqs = {p: sum(freqs[source] for source in pair_sources[p]) for p in freqs}
    count = {element: 0 for pair in freqs for element in pair}
    for pair, freq in freqs.items():
        count[pair[0]] += freq
        count[pair[1]] += freq
    # All elements have been counted in pairs, EXCEPT for the first and last in the template
    return [(value + 1) // 2 for value in count.values()]


print("Part 1", (lambda count: max(count) - min(count))(generate_element_count(frequencies, 10)))
print("Part 2", (lambda count: max(count) - min(count))(generate_element_count(frequencies, 40)))
