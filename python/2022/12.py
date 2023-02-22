"""Hill Climbing Algorithm"""

def dijkstra(height, start, targets, graph):
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


def reachable(source, dest, height):
    if source not in height or dest not in height:
        return False
    step = source - dest
    if abs(step.real) + abs(step.imag) > 1:
        return False
    climb = height[dest] - height[source]
    if climb > 1:
        return False
    return True


def neighbours(z):
    for dz in [1, -1, 1j, -1j]:
        yield z + dz


def get_height(char):
    match char:
        case "S":
            return ord("a")
        case "E":
            return ord("z")
        case _:
            return ord(char)


def solve(text):
    landscape = {
        complex(r, c): char
        for r, line in enumerate(text.strip().splitlines())
        for c, char in enumerate(line)
    }
    height = {z: get_height(char) for z, char in landscape.items()}
    start = next(z for z, char in landscape.items() if char == "S")
    end = next(z for z, char in landscape.items() if char == "E")

    graph = {p: [n for n in neighbours(p) if reachable(p, n, height)] for p in height}
    yield dijkstra(height, start, [end], graph)

    bottoms = [z for z, char in landscape.items() if char == "a"]
    graph = {p: [n for n in neighbours(p) if reachable(n, p, height)] for p in height}
    yield dijkstra(height, end, bottoms, graph)
