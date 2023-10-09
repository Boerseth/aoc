"""Wizard Simulator 20XX"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Iterator, NamedTuple


@dataclass
class Spell:
    name: str
    cost: int
    effects: list[tuple[str, int]]


Missile = Spell("missile", 53, effects=[("boss_hp", -4)])
Drain = Spell("drain", 73, effects=[("boss_hp", -2), ("hp", +2)])
Shield = Spell("shield", 113, effects=[("shield", 6)])
Poison = Spell("poison", 173, effects=[("poison", 6)])
Recharge = Spell("recharge", 229, effects=[("recharge", 5)])
SPELLS = [
    Missile,
    Drain,
    Shield,
    Poison,
    Recharge
]


@dataclass
class State:
    hp: int
    mana: int
    boss_hp: int
    boss_damage: int
    shield: int = 0
    poison: int = 0
    recharge: int = 0
    mana_spent: int = 0
    mana_limit: int | None = None
    history: tuple = ()

    def is_win(self) -> bool:
        return self.boss_hp <= 0

    def is_lose(self) -> bool:
        return self.hp <= 0

    def is_over(self) -> bool:
        return self.is_lose() or self.is_win()

    @classmethod
    def _from(cls, other: State) -> State:
        return cls(**asdict(other))

    def copy(self) -> State:
        return self._from(self)

    def start_turn(self) -> None:
        self.boss_hp -= 3 * bool(self.poison)
        self.mana += 101 * bool(self.recharge)
        self.shield = max(0, self.shield - 1)
        self.poison = max(0, self.poison - 1)
        self.recharge = max(0, self.recharge - 1)

    def can_cast(self, spell: Spell) -> bool:
        if spell.cost > self.mana:
            return False
        if self.mana_limit is not None and spell.cost >= self.mana_limit - self.mana_spent:
            return False
        if hasattr(self, spell.name) and bool(getattr(self, spell.name)):
            return False
        return True

    def cast(self, spell: spell) -> None:
        assert self.can_cast(spell)
        self.history = (*self.history, spell.name)
        self.mana -= spell.cost
        self.mana_spent += spell.cost
        for key, val in spell.effects:
            setattr(self, key, getattr(self, key) + val)

    def boss(self) -> None:
        self.hp -= max(1, self.boss_damage - 7 * bool(self.shield))

    def maybe_possible_to_win(self) -> None:
        if not self.mana_limit:
            return True

        allowed = self.mana_limit - self.mana_spent
        boss_hp = self.boss_hp
        poison = self.poison

        # Simulate doing all the damage in the world regardless of HP or mana
        while allowed >= 53:
            # Wiz' turn
            boss_hp -= 3 * bool(poison)
            poison = max(0, poison - 1)
            if (allowed >= 173 + 53) and poison == 0:
                allowed -= 173
                poison = 6
            else:
                allowed -= 53
                boss_hp -= 4
            # Boss' turn
            boss_hp -= 3 * bool(poison)
            poison = max(0, poison - 1)
            if boss_hp <= 0:
                return True
        return False


def do_turn(state: State, turn: int = 0, hard_mode: bool = False) -> Iterator[int]:
    assert not state.is_win()
    assert not state.is_lose()
    assert not state.is_over()
    assert state.mana_limit is None or state.mana_spent < state.mana_limit

    if ((turn % 2) == 0) and hard_mode:
        state.hp -= 1
        if state.is_lose():
            return

    state.start_turn()
    if state.is_over():
        if state.is_win():
            yield state
        return

    if turn % 2:
        state.boss()
        if not state.is_over():
            yield from do_turn(state, turn + 1, hard_mode)
        if state.is_win():
            yield state
        return

    if not state.maybe_possible_to_win():
        return

    for spell in sorted(SPELLS, key=lambda s: s.cost):
        if not state.can_cast(spell):
            continue

        new_state = state.copy()
        new_state.cast(spell)
        if new_state.is_win():
            state.mana_limit = new_state.mana_spent
            yield new_state
            continue

        for win_state in do_turn(new_state, turn + 1, hard_mode):
            if state.mana_limit and win_state.mana_spent >= state.mana_limit:
                continue
            state.mana_limit = new_state.mana_limit = win_state.mana_spent
            yield win_state


def solve(text: str) -> Iterator:
    boss_stats = [int(s) for s in text.strip().split()[2::2]]

    state = State(
        hp=50,
        mana=500,
        boss_hp=boss_stats[0],
        boss_damage=boss_stats[1],
    )

    for hard_mode in [False, True]:
        yield min(s.mana_spent for s in do_turn(state.copy(), hard_mode=hard_mode))
