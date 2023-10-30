"""Some Assembly Required"""


class Circuit:
    def __init__(self):
        self.potentials = {}

    def get(self, key: str) -> int | None:
        if key.isdigit():
            return int(key)
        return self.potentials.get(key)

    def _not(self, source: str) -> None:
        if val := self.get(source):
            return ~ val

    def _and(self, source1: str, source2: str) -> int | None:
        val1 = self.get(source1)
        val2 = self.get(source2)
        if val1 is not None and val2 is not None:
            return val1 & val2

    def _or(self, source1: str, source2: str) -> int | None:
        val1 = self.get(source1)
        val2 = self.get(source2)
        if val1 is not None and val2 is not None:
            return val1 | val2

    def lshift(self, source1: str, source2: str) -> int | None:
        val1 = self.get(source1)
        val2 = self.get(source2)
        if val1 is not None and val2 is not None:
            return (val1 << val2) % 2 ** 16

    def rshift(self, source1: str, source2: str) -> int | None:
        val1 = self.get(source1)
        val2 = self.get(source2)
        if val1 is not None and val2 is not None:
            return (val1 >> val2) % 2 ** 16

    def set(self, key: str, value: int | None) -> None:
        if value is not None:
            self.potentials[key] = value

    def turn_on_potentials(self, instructions: list[tuple[str, str]]) -> None:
        iterations_since_last_update = 0
        while instructions and iterations_since_last_update <= len(instructions):
            expression, target = instructions.pop(0)
            if self.get(target) is not None:
                continue
            match expression.split():
                case source,:
                    self.set(target, self.get(source))
                case "NOT", source:
                    self.set(target, self._not(source))
                case source1, "AND", source2:
                    self.set(target, self._and(source1, source2))
                case source1, "OR", source2:
                    self.set(target, self._or(source1, source2))
                case source1, "LSHIFT", source2:
                    self.set(target, self.lshift(source1, source2))
                case source1, "RSHIFT", source2:
                    self.set(target, self.rshift(source1, source2))
                case _:
                    pass
            if self.get(target) is None:
                instructions.append((expression, target))
                iterations_since_last_update += 1
            else:
                iterations_since_last_update = 0

        # Remaining wires are not hooked up to anything. Define them as grounded.
        for _, target in instructions:
            self.set(target, 0)
        # But really, all instructions are used:
        assert not instructions


def solve(text):
    instructions = [line.strip().split(" -> ") for line in text.splitlines()]

    circuit1 = Circuit()
    circuit1.turn_on_potentials([i for i in instructions])
    yield circuit1.get("a")

    circuit2 = Circuit()
    circuit2.set("b", circuit1.get("a"))
    circuit2.turn_on_potentials([i for i in instructions])
    yield circuit2.get("a")
