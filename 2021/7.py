    positions = list(map(int, open("input_7", "r").readline().split(",")))
    
    
    def cost_1(horizontal_goal):
        return sum(abs(pos - horizontal_goal) for pos in positions)
    
    
    def cost_2(goal):
        return sum((abs(pos - goal) * (abs(pos - goal) + 1)) // 2 for pos in positions)
    
    
    low = min(positions)
    high = max(positions)
    
    
    print("Part 1:", min(cost_1(i) for i in range(low, high + 1)))
    print("Part 2:", min(cost_2(i) for i in range(low, high + 1)))
