def solve():
    positions = list(map(int, open("inputs/7", "r").readline().split(",")))
    low = min(positions)
    high = max(positions)

    def cost_1(horizontal_goal):
        return sum(abs(pos - horizontal_goal) for pos in positions)

    def cost_2(goal):
        return sum((abs(pos - goal) * (abs(pos - goal) + 1)) // 2 for pos in positions)

    yield min(cost_1(i) for i in range(low, high + 1))
    yield min(cost_2(i) for i in range(low, high + 1))


def solutions():
    yield 347011
    yield 98363777


if __name__ == "__main__":
    from helpers import main_template

    main_template(solve, solutions)
