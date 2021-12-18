if True:
    data = [line.strip() for line in open("input_10", "r").readlines()]
    bracket_match = {")": "(", "]": "[", "}": "{", ">": "<"}

    # Part 1
    def find_corruption_score(line):
        error_points = {")": 3, "]": 57, "}": 1197, ">": 25137}
        seen_so_far = []
        for c in line:
            if c not in bracket_match:
                # c is an opener
                seen_so_far.append(c)
            elif seen_so_far.pop(-1) != bracket_match[c]:
                return error_points[c]
        return 0

    # Part 2
    def find_completion_score(line):
        completion_points = {"(": 1, "[": 2, "{": 3, "<": 4}
        seen_so_far = []
        for c in line:
            if c not in bracket_match:
                # c is an opener
                seen_so_far.append(c)
            else:
                seen_so_far.pop(-1)

        total = 0
        for c in reversed(seen_so_far):
            total *= 5
            total += completion_points[c]
        return total

    incomplete_lines = [line for line in data if find_corruption_score(line) == 0]
    sorted_scores = sorted([find_completion_score(line) for line in incomplete_lines])
    print("Part 1:", sum(find_corruption_score(line) for line in data))
    print("Part 2:", sorted_scores[len(sorted_scores) // 2])
