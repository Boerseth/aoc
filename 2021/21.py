def solve(text):
    line_1, line_2 = text.strip().splitlines()
    start_1 = int(line_1.split(": ")[1].strip())
    start_2 = int(line_2.split(": ")[1].strip())

    pos_1 = start_1
    pos_2 = start_2
    points_1 = 0
    points_2 = 0
    die = 1
    rolls = 0
    player_1_turn = True
    while points_1 < 1000 and points_2 < 1000:
        if player_1_turn:
            pos_1 = 1 + (pos_1 + 3 * die + 2) % 10
            points_1 += pos_1
        else:
            pos_2 = 1 + (pos_2 + 3 * die + 2) % 10
            points_2 += pos_2
        player_1_turn = not player_1_turn
        die = 1 + (die + 2) % 100
        rolls += 3
    yield rolls * min(points_1, points_2)


    cache = {}
    def outcome_freqs(*args):
        if args in cache:
            return cache[args]
        start_1, start_2, pos_1, pos_2, scr_1, scr_2, player_1_turn = args

        if scr_1 < 0 or scr_2 < 0 or (player_1_turn and scr_2 > 20) or (not player_1_turn and scr_1 > 20):
            return 0
        if scr_1 == scr_2 == 0:
            return int(pos_1 == start_1 and pos_2 == start_2 and not player_1_turn)

        freq = 0
        for i in range(3, 10):
            mult = {3: 1, 4: 3, 5: 6, 6: 7, 7: 6, 8: 3, 9: 1}[i]
            if scr_2 < 21 and player_1_turn:
                pos_1_prev = 1 + (pos_1 - 1 - i) % 10
                scr_1_prev = scr_1 - pos_1
                freq += mult * outcome_freqs(start_1, start_2, pos_1_prev, pos_2, scr_1_prev, scr_2, False)
            if scr_1 < 21 and not player_1_turn:
                pos_2_prev = 1 + (pos_2 - 1 - i) % 10
                scr_2_prev = scr_2 - pos_2
                freq += mult * outcome_freqs(start_1, start_2, pos_1, pos_2_prev, scr_1, scr_2_prev, True)
        cache[(start_1, start_2, pos_1, pos_2, scr_1, scr_2, player_1_turn)] = freq
        return freq


    player_1_wins = sum(
        outcome_freqs(start_1, start_2, pos_1, pos_2, j, i, False)
        for pos_1 in range(1, 11)
        for pos_2 in range(1, 11)
        for i in range(21, 31)
        for j in range(21)
    )
    player_2_wins = sum(
        outcome_freqs(10, 9, pos_1, pos_2, i, j, True)
        for pos_1 in range(1, 11)
        for pos_2 in range(1, 11)
        for i in range(21, 31)
        for j in range(21)
    )
    yield max(player_1_wins, player_2_wins)


if __name__ == "__main__":
    from helpers import main_template

    main_template("21", solve)

"""

quit()


# Below is a more inefficient way of doing part 2


def get_ppss():
    for position_1 in range(1, 11):
        for position_2 in range(1, 11):
            for score_1 in range(31):
                for score_2 in range(31):
                    yield position_1, position_2, score_1, score_2

start_1 = 10
start_2 = 9

universes = {}
for ppss in get_ppss():
    universes[ppss] = 0
universes[(start_1, start_2, 0, 0)] = 1


for roll in range(40):
    next_universes = {ppss: 0 for ppss in get_ppss()}
    for position_1, position_2, score_1, score_2 in get_ppss():
        freq = universes[(position_1, position_2, score_1, score_2)]
        if score_1 < 21 and score_2 < 21:
            for i in range(3, 10):
                pos_1_next = position_1
                pos_2_next = position_2
                scr_1_next = score_1
                scr_2_next = score_2
                if roll % 2 == 0:
                    pos_1_next = 1 + (position_1 - 1 + i) % 10
                    scr_1_next = score_1 + pos_1_next
                else:
                    pos_2_next = 1 + (position_2 - 1 + i) % 10
                    scr_2_next = score_2 + pos_2_next
                ppss = (pos_1_next, pos_2_next, scr_1_next, scr_2_next)
                mult = {3: 1, 4: 3, 5: 6, 6: 7, 7: 6, 8: 3, 9: 1}[i]
                next_universes[ppss] += mult * freq
        else:
            next_universes[(position_1, position_2, score_1, score_2)] += freq
    universes = {key: value for key, value in next_universes.items()}

score_1 = sum(freq for (pos1, pos2, scr1, scr2), freq in universes.items() if scr1 > 20)
score_2 = sum(freq for (pos1, pos2, scr1, scr2), freq in universes.items() if scr2 > 20)
print("Part 2:", max(score_1, score_2))
"""
