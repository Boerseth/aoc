cave_system = [line.strip().split("-") for line in open("input_12", "r").readlines()]
movement_choices = {cave: set() for cave in {cave for edge in cave_system for cave in edge}}
for cave_1, cave_2 in cave_system:
    if cave_2 != "start":
        movement_choices[cave_1].add(cave_2)
    if cave_1 != "start":
        movement_choices[cave_2].add(cave_1)


def should_use_updated_map(next_position, visited, can_revisit_small):
    if not can_revisit_small:
        return True
    if next_position in visited and next_position.islower():
        return True
    return False


cache = {}
def find_number_of_paths(position, move_choice_map, visited, can_revisit_small):
    key = (position, "".join(sorted(visited)), can_revisit_small)
    if key in cache:
        return cache[key]

    assert visited[-1] == position
    if position == "end":
        return 1

    number_of_paths = 0
    for next_position in move_choice_map[position]:
        if should_use_updated_map(next_position, visited, can_revisit_small):
            next_can_revisit_small = False
            next_move_choice_map = {
                cave: {c for c in choices if c not in visited or c.isupper()}
                for cave, choices in move_choice_map.items()
            }
        else:
            next_can_revisit_small = can_revisit_small
            next_move_choice_map = move_choice_map

        number_of_paths += find_number_of_paths(
            next_position,
            next_move_choice_map,
            visited + [next_position],
            next_can_revisit_small,
        )
    cache[key] = number_of_paths

    return cache[key]


print("Part 1:", find_number_of_paths("start", movement_choices, ["start"], False))
print("Part 2:", find_number_of_paths("start", movement_choices, ["start"], True))
