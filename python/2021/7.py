def solve(text):
    positions = list(map(int, text.strip().split(",")))
    low = min(positions)
    high = max(positions)

    def cost_1(horizontal_goal):
        return sum(abs(pos - horizontal_goal) for pos in positions)

    def cost_2(goal):
        return sum((abs(pos - goal) * (abs(pos - goal) + 1)) // 2 for pos in positions)

    yield min(cost_1(i) for i in range(low, high + 1))
    yield min(cost_2(i) for i in range(low, high + 1))
