dirs = [{"^": 1j, ">": 1, "v": -1j, "<": -1}[c] for c in open("input_3", "r").readline().strip()]


# Part 1:
print("Part 1:", len(set(sum(dirs[:i]) for i in range(len(dirs) + 1))))


# Part 2:
visited_by_santa = set(sum(dirs[: 2 * i : 2]) for i in range(len(dirs[::2]) + 1))
visited_by_robos = set(sum(dirs[1 : 2 * i : 2]) for i in range(len(dirs[1::2]) + 1))
print("Part 2:", len(visited_by_santa | visited_by_robos))
