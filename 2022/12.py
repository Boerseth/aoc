def dijkstra(elavation, start, targets, graph):
    R = len(elavation)
    C = len(elavation[0])

    distances = {start: 0}
    unvisited = {0: [start]}
    while not any(t in distances for t in targets):
        currents = unvisited.pop(min(unvisited.keys()))
        for current in currents:
            current_distance = distances[current]
            neigh_distance = current_distance + 1
            for neigh in graph[current]:
                if neigh in distances and distances[neigh] <= neigh_distance:
                    continue
                distances[neigh] = neigh_distance
                unvisited[neigh_distance] = unvisited.get(neigh_distance, []) + [neigh]
    return next(distances[t] for t in targets if t in distances)


def manhattan_distance(start, end):
    r_start, c_start = start
    r_end, c_end = end
    return abs(r_start - r_end) + abs(c_start - c_end)


def reachable(source, destination, elavation):
    r_source, c_source = source
    r_dest, c_dest = destination
    return (
        manhattan_distance(source, destination) == 1
        and elavation[r_dest][c_dest] - elavation[r_source][c_source] <= 1
    )


def neighbours(position, R, C):
    r, c = position
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        if 0 <= r + dr < R and 0 <= c + dc < C:
            yield r + dr, c + dc


def get_elavation(char):
    match char:
        case "S": return ord("a")
        case "E": return ord("z")
        case _: return ord(char)


def solve(text):
    _map = [list(line) for line in text.strip().splitlines()]
    R = len(_map)
    C = len(_map[0])
    rc_pairs = [(r, c) for r in range(R) for c in range(C)]
    elavation = [[get_elavation(char) for char in row] for row in _map]

    start = next((r, c) for r, c in rc_pairs if _map[r][c] == "S")
    end = next((r, c) for r, c in rc_pairs if _map[r][c] == "E")
    graph = {p: [n for n in neighbours(p, R, C) if reachable(p, n, elavation)] for p in rc_pairs}
    yield dijkstra(elavation, start, [end], graph)

    bottoms = [(r, c) for r, c in rc_pairs if _map[r][c] == "a"]
    graph = {p: [n for n in neighbours(p, R, C) if reachable(n, p, elavation)] for p in rc_pairs}
    yield dijkstra(elavation, end, bottoms, graph)


def solutions():
    yield 528
    yield 522


if __name__ == "__main__":
    from helpers import main_template

    with open("inputs/12", "r") as f:
        text = f.read()
    main_template(lambda: solve(text), solutions)
