"""Lanternfish"""

def next_timer_state(timer):
    if timer >= 7:
        return timer - 1
    return (timer - 1) % 7


def spawn(timers, days_to_go):
    if days_to_go == 0:
        return timers
    return spawn(
        [next_timer_state(timer) for timer in timers] + [8 for timer in timers if timer == 0],
        days_to_go - 1,
    )


# Off-by-one is a bitch, so take these recursion formulae with a fistful of salt
# P(i, d) = | 1 if i >= d
#           | else P(0, d-1)
#
# P(0, d) = | 1 if 0 >= d
#           | else P(6, d-1) + P(8, d-1)
#
# P(6, d-1) + P(8, d-1) = | 1 + P(8, d-1) if 6 >= d-1
#                         | P(6, d-8) + P(8, d-1) + P(8, d-8)
#
# etc. for roof((d-1)/7) child families
cache = {}
def size_of_family_new(initial_state, days_to_go):
    if initial_state > 0:
        return size_of_family_new(0, days_to_go - initial_state)
    if days_to_go <= 0:
        return 1
    if not days_to_go in cache:
        cache[days_to_go] = 1 + sum(
            # Add size of each family for every child that the fish will have
            size_of_family_new(8, days_to_go - 1 - 7 * generation)
            for generation in range((days_to_go - 1) // 7 + 1)
        )
    return cache[days_to_go]


def smart_spawn(lanternfish_timers, days_to_go):
    return sum(size_of_family_new(fish, days_to_go) for fish in lanternfish_timers)


def solve(text):
    initial_state = [int(num) for num in text.strip().split(",")]
    # print("Part 1:", len(spawn(initial_state, 80)))
    yield smart_spawn(initial_state, 80)
    yield smart_spawn(initial_state, 256)
