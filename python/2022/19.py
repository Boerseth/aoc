"""Not Enough Minerals"""


def have_enough(robot_type, robot_count, blueprint):
    return all(recipe[robot_type] <= robot_count for recipe in blueprint)


def can_get_resources(robots, recipe):
    return all(have or not need for have, need in zip(robots, recipe))


def get_available_strategies(blueprint, robots, time_left):
    # Ore and Clay only require Ore to build, so we can get enough resources
    if not have_enough(0, robots[0], blueprint):
        yield 0
    if not have_enough(1, robots[1], blueprint):
        yield 1
    if not have_enough(2, robots[2], blueprint) and can_get_resources(robots, blueprint[2]):
        yield 2
    if can_get_resources(robots, blueprint[3]):
        yield 3


def build_robot(blueprint, resources, robots, robot):
    resources = [resource - required for resource, required in zip(resources, blueprint[robot])]
    robots[robot] += 1
    return resources, robots


def can_build_robot(blueprint, resources, robot):
    recipe = blueprint[robot]
    return all(required <= resource for required, resource in zip(recipe, resources))


def should_give_up(resources, robots, time_left, max_so_far):
    if max_so_far is None:
        return False
    geo = resources[3]
    robot_geo = robots[3]
    upper_bound = geo + time_left * robot_geo + (time_left * (time_left - 1)) // 2
    return upper_bound <= max_so_far


def find_max_geodes(blueprint, resources, robots, next_robot, time_left, max_so_far=None):
    if time_left <= 0:
        return resources[3]
    if should_give_up(resources, robots, time_left, max_so_far):
        return 0

    can_build_next_robot = can_build_robot(blueprint, resources, next_robot)
    # The rule is dumb, but you must check before mining
    resources = [res + mined for res, mined in zip(resources, robots)]

    if not can_build_next_robot:
        # Todo: Compute how many minutes until can_build, then just skip to that
        return find_max_geodes(
            blueprint, [*resources], [*robots], next_robot, time_left - 1, max_so_far
        )

    resources, robots = build_robot(blueprint, resources, robots, next_robot)
    for next_next_robot in get_available_strategies(blueprint, robots, time_left):
        geode_count = find_max_geodes(
            blueprint, [*resources], [*robots], next_next_robot, time_left - 1, max_so_far
        )
        if max_so_far is None or (geode_count is not None and max_so_far < geode_count):
            max_so_far = geode_count
    return max_so_far


def find_max_geodes_per_init_cond(blueprint, time):
    return max(
        find_max_geodes(blueprint, [0, 0, 0, 0], [1, 0, 0, 0], r, time)
        for r in range(len(blueprint))
    )


def parse_line(line):
    title, recipes = line.split(": ")
    bp_id = int(title.split()[1])

    ROBOTS = ["ore", "clay", "obsidian", "geode"]
    blueprint = []
    for recipe_text in recipes.split(". "):
        recipe = {r: 0 for r in ROBOTS}

        match recipe_text.split():
            case "Each", _, "robot", "costs", count, rock:
                recipe |= {rock: int(count)}
            case "Each", _, "robot", "costs", count1, rock1, "and", count2, rock2:
                recipe |= {rock1: int(count1), rock2.rstrip("."): int(count2)}

        blueprint.append([recipe[r] for r in ROBOTS])

    return {"id": bp_id, "bp": blueprint}


def solve(text):
    blueprints = [parse_line(l) for l in text.splitlines()]

    yield sum(bp["id"] * find_max_geodes_per_init_cond(bp["bp"], 24) for bp in blueprints)

    product = 1
    for bp in blueprints[:3]:
        product *= find_max_geodes_per_init_cond(bp["bp"], 32)
    yield product
