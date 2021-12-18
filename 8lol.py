lines = [line.strip() for line in open("input_8", "r").readlines()]


# Part 1
print("Part 1:", sum(sum(1 for word in line.split(" | ")[1].split() if len(word) in [2, 3, 4, 7]) for line in lines))


# Part 2
def interpret(line):
    digits = line.split(" | ")[0].split()

    one = [d for d in digits if len(d) == 2].pop()
    seven = [d for d in digits if len(d) == 3].pop()
    four = [d for d in digits if len(d) == 4].pop()
    eight = [d for d in digits if len(d) == 7].pop()

    two_three_five = [d for d in digits if len(d) == 5]
    three = [d for d in two_three_five if all(s not in one for s in [c for c in eight if c not in d])].pop()
    two = [d for d in two_three_five if sorted(list({c for c in d + four})) == sorted(list(c for c in eight))].pop()
    five = [d for d in two_three_five if d not in [two, three]].pop()

    zero_six_nine = [d for d in digits if len(d) == 6]
    nine = [d for d in zero_six_nine if [s for s in eight if s not in d].pop() not in four].pop()
    zero_six = [d for d in zero_six_nine if d != nine]
    six = [d for d in zero_six_nine if [s for s in eight if s not in d].pop() in one].pop()
    zero = [d for d in zero_six if d != six].pop()

    lookup = {
        "".join(sorted(zero)): "0",
        "".join(sorted(one)): "1",
        "".join(sorted(two)): "2",
        "".join(sorted(three)): "3",
        "".join(sorted(four)): "4",
        "".join(sorted(five)): "5",
        "".join(sorted(six)): "6",
        "".join(sorted(seven)): "7",
        "".join(sorted(eight)): "8",
        "".join(sorted(nine)): "9",
    }

    return int("".join(lookup["".join(sorted(d))] for d in line.split(" | ")[1].split()))

print("Part 2:", sum(interpret(line) for line in lines))
