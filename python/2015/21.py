"""RPG Simulator 20XX"""
from typing import Iterator


TABLEDATA = """
Weapons:    Cost  Damage  Armor
Dagger        8     4       0
Shortsword   10     5       0
Warhammer    25     6       0
Longsword    40     7       0
Greataxe     74     8       0

Armor:      Cost  Damage  Armor
Leather      13     0       1
Chainmail    31     0       2
Splintmail   53     0       3
Bandedmail   75     0       4
Platemail   102     0       5

Rings:      Cost  Damage  Armor
Damage +1    25     1       0
Damage +2    50     2       0
Damage +3   100     3       0
Defense +1   20     0       1
Defense +2   40     0       2
Defense +3   80     0       3
"""


def parse_table(table):
    head, *rows = table.splitlines()
    return sorted([list(map(int, row.split()[-3:])) for row in rows], key=lambda r: r[0])


weapons, armors, rings = map(parse_table, TABLEDATA.strip().split("\n\n"))


def would_win(boss_stats, stats) -> bool:
    boss_hp, boss_damage, boss_armor = boss_stats
    char_hp, char_damage, char_armor = stats
    boss_attack = max(1, boss_damage - char_armor)
    char_attack = max(1, char_damage - boss_armor)
    boss_ttl = int(boss_hp / char_attack) + bool(boss_hp % char_attack)
    char_ttl = int(char_hp / boss_attack) + bool(char_hp % boss_attack)
    return boss_ttl <= char_ttl


def solve(text: str) -> Iterator:
    assert would_win([104, 8, 1], [100, 6, 4])
    boss_stats = [int(line.split()[-1]) for line in text.strip().splitlines()]

    min_cost = sum(cost for cost, _, _ in weapons + armors + rings)
    for weapon in weapons:
        if min_cost <= weapon[0]:
            break
        for armor in [[0, 0, 0]] + armors:
            if min_cost <= weapon[0] + armor[0]:
                break
            for ring1 in [[0, 0, 0]] + rings:
                if min_cost <= weapon[0] + armor[0] + ring1[0]:
                    break
                for ring2 in [[0, 0, 0]] + rings:
                    cost, damage, defense = [sum(spec) for spec in zip(weapon, armor, ring1, ring2)]
                    if cost >= min_cost:
                        continue
                    if would_win(boss_stats, [100, damage, defense]):
                        min_cost = cost
                        break
    yield min_cost

    max_cost = 0
    for weapon in weapons[::-1]:
        for armor in armors[::-1] + [[0, 0, 0]]:
            for ring1 in rings[::-1] + [[0, 0, 0]]:
                for ring2 in rings[::-1] + [[0, 0, 0]]:
                    if ring1[0] and ring2[0] and ring1[0] >= ring2[0]:
                        break
                    cost, damage, defense = [sum(spec) for spec in zip(weapon, armor, ring1, ring2)]
                    if cost <= max_cost:
                        continue
                    if not would_win(boss_stats, [100, damage, defense]):
                        max_cost = cost
                        break
    yield max_cost
