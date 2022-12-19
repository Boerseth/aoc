def neighbours(r):
    x, y, z = r
    for dc in [-1, 1]:
        yield x + dc, y, z
        yield x, y + dc, z
        yield x, y, z + dc


def neighbour_set(other_set):
    return {neigh for element in other_set for neigh in neighbours(element)} - other_set


def find_outer_shell(cubes):
    outer_shell = set()
    neighbourhood = neighbour_set(cubes)
    # Start exploring at some extremal outer cube - e.g. in x-direction:
    frontier = {min(neighbourhood, key=lambda c: c[0])}
    while frontier:
        frontier |= neighbour_set(frontier) - cubes
        frontier |= neighbour_set(frontier) - cubes

        discovered = (frontier & neighbourhood) - outer_shell
        outer_shell |= discovered
        frontier = discovered
    return outer_shell


def solve(text):
    cubes = {tuple(int(c) for c in line.split(",")) for line in text.splitlines()}
    yield sum(1 for c in cubes for n in neighbours(c) if n not in cubes)

    outer_shell = find_outer_shell(cubes)
    yield sum(1 for s in outer_shell for n in neighbours(s) if n in cubes)


if __name__ == "__main__":
    from helpers import main_template

    main_template("18", solve)
