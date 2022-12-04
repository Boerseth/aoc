cache = {}
def find_number_of_paths(position, move_choices, visited, permitted_small_revisits):
    key = (position, "".join(sorted(visited)), permitted_small_revisits)
    if key in cache:
        return cache[key]

    small_revisits = sum(visited.count(cave) - 1 for cave in set(visited) if cave.islower())
    if position.islower() and position in visited and small_revisits == permitted_small_revisits:
        return 0

    if position == "end":
        return 1

    number_of_paths = 0
    for next_position in move_choices[position]:
        number_of_paths += find_number_of_paths(
            next_position,
            move_choices,
            visited + [position],
            permitted_small_revisits,
        )
    cache[key] = number_of_paths

    return cache[key]


def solve():
    cave_system = [line.strip().split("-") for line in open("inputs/12", "r").readlines()]
    movement_choices = {cave: set() for cave in {cave for edge in cave_system for cave in edge}}
    for cave_1, cave_2 in cave_system:
        if cave_2 != "start":
            movement_choices[cave_1].add(cave_2)
        if cave_1 != "start":
            movement_choices[cave_2].add(cave_1)
    yield find_number_of_paths("start", movement_choices, [], 0)
    yield find_number_of_paths("start", movement_choices, [], 1)


def solutions():
    yield 5576
    yield 152837


if __name__ == "__main__":
    from helpers import main_template

    main_template(solve, solutions)
