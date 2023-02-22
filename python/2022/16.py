START = "AA"


def prune_nodes_with_no_pressure(graph, rewards):
    for node in list(graph.keys()):
        if rewards.get(node):
            continue
        if node not in graph:
            continue

        neighbours = graph[node]
        if len(neighbours) != 2:
            continue

        (neigh1, dist1), (neigh2, dist2) = neighbours.items()
        dist = dist1 + dist2
        if neigh2 not in graph[neigh1] or dist < graph[neigh1][neigh2]:
            graph[neigh1][neigh2] = dist
        if neigh1 not in graph[neigh2] or dist < graph[neigh2][neigh1]:
            graph[neigh2][neigh1] = dist

        graph.pop(node)
        graph[neigh1].pop(node)
        graph[neigh2].pop(node)
    return graph


def generate_graph_without_middle_steps(graph):
    # Distance to neighbours becomes 2, because we assume that going there also
    # implies spending a minute to turn on the valve
    direct_graph = {key: {k: v + 1 for k, v in val.items()} for key, val in graph.items()}

    nodes = list(graph)
    updated_nodes = set(nodes)
    while updated_nodes:
        next_updated_nodes = set()
        for node in updated_nodes:
            # `node` had some of its distances updated last time.
            # Check if any of its neighbours now has a shorter path
            # to another neighbour through `node`.
            neighbours = list(direct_graph[node].items())
            for neigh1, dist1 in neighbours:
                for neigh2, dist2 in neighbours:
                    if neigh1 == neigh2:
                        continue
                    # Subtract 1, as this is the distance for traversing dist1, but
                    # skipping the valve at `node`
                    new_distance = dist1 - 1 + dist2
                    if (
                        neigh2 not in direct_graph[neigh1]
                        or new_distance < direct_graph[neigh1][neigh2]
                    ):
                        direct_graph[neigh1][neigh2] = new_distance
                        next_updated_nodes.add(neigh1)
                    if (
                        neigh1 not in direct_graph[neigh2]
                        or new_distance < direct_graph[neigh2][neigh1]
                    ):
                        direct_graph[neigh2][neigh1] = new_distance
                        next_updated_nodes.add(neigh2)
        updated_nodes = next_updated_nodes
    return direct_graph


def traverse_graph(direct_graph, valve_pressure, path, banned, cumulative_pressure, time_left):
    skip = set(path + banned)
    for node, dist in direct_graph[path[-1]].items():
        if node in skip:
            continue
        new_time_left = time_left - dist
        if new_time_left < 0:
            continue

        new_cumulative_pressure = cumulative_pressure + new_time_left * valve_pressure[node]
        new_path = path + [node]
        yield new_cumulative_pressure, new_path
        yield from traverse_graph(
            direct_graph, valve_pressure, new_path, banned, new_cumulative_pressure, new_time_left
        )


def find_optimal_path_and_pressure(graph, valve_pressure, banned, time):
    max_pressure, optimal_path = 0, None
    for pressure, path in traverse_graph(graph, valve_pressure, [START], banned, 0, time):
        if max_pressure >= pressure:
            continue
        max_pressure = pressure
        optimal_path = path
    return max_pressure, optimal_path


def parse_line(line):
    match line.replace("=", " ").replace(";", "").replace(",", "").split():
        case "Valve", valve, "has", "flow", "rate", rate, _, _, "to", _, *neighbours:
            return valve, int(rate), neighbours


def solve(text, timer=None):
    valve_data = [parse_line(line) for line in text.splitlines()]
    initial_graph = {valve: {n: 1 for n in neighbours} for valve, _, neighbours in valve_data}
    valve_pressure = {valve: rate for valve, rate, _ in valve_data}

    pruned_graph = prune_nodes_with_no_pressure(initial_graph, valve_pressure)
    graph = generate_graph_without_middle_steps(pruned_graph)

    max_pressure, path = find_optimal_path_and_pressure(graph, valve_pressure, [], 30)
    yield max_pressure

    # For whatever reason, the gready approach works:
    # pressure1, path1 = find_optimal_path_and_pressure(graph, valve_pressure, [], 26)
    # pressure2, path2 = find_optimal_path_and_pressure(graph, valve_pressure, path1, 26)
    # yield pressure1 + pressure2

    # Make more robust:
    # First find optimal path for single traveller within given
    # time, and find the optimal path for other traveller given
    # remaining nodes.
    #
    # Then, solve over again, but gradually ban nodes in path1
    # for the first traveller. If len(path1) == N, then there
    # will be 2 ** N such subsets to be banned.
    # However, we might not have to explore all of them, as some
    # subsets might contain previous ones, and be contained them-
    # self by the avoided nodes in path that resulted:
    #   banned_0 < banned_1 < avoided_0
    # In those two conditions apply, then the optimal path from
    # banned_1 will be the same as that from banned_0.
    # This might reduce the number of partitions to check enough
    # to make the problem solvable within a short time.
    pressure1, unrestricted_path = find_optimal_path_and_pressure(graph, valve_pressure, [], 26)
    pressure2, other_path = find_optimal_path_and_pressure(
        graph, valve_pressure, unrestricted_path, 26
    )

    nodes = sorted(unrestricted_path)
    banned_avoided_pressure = [(0, 0, pressure1 + pressure2)]
    for i in range(2 ** len(nodes)):
        if any(b & i == b and i & a == i for b, a, _ in banned_avoided_pressure):
            continue
        banned = [node for n, node in enumerate(nodes) if (1 << n) & i]
        pressure1, path1 = find_optimal_path_and_pressure(graph, valve_pressure, banned, 26)
        avoided = sum(2**n for n, node in enumerate(nodes) if node not in path1)
        pressure2, path2 = find_optimal_path_and_pressure(graph, valve_pressure, path1, 26)
        banned_avoided_pressure.append((i, avoided, pressure1 + pressure2))

    pressures = [p for _, _, p in banned_avoided_pressure]
    yield max(pressures)


if __name__ == "__main__":
    from helpers import main_template

    main_template("16", solve)
