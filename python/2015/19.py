"""Medicine for Rudolph"""
import json
from typing import Iterator


def parse(text: str) -> tuple[dict[str, list[str]], str]:
    replacements, molecule = text.split("\n\n")
    lookup = {}
    for replacement in replacements.strip().splitlines():
        start, _, end = replacement.split()
        lookup.setdefault(start, list()).append(end)
    return lookup, molecule.strip()


def apply_replacements(molecule: str, replacements: dict[str, list[str]]) -> set[str]:
    return {
        molecule[:index] + child + molecule[index + len(parent) :]
        for parent, children in replacements.items()
        for child in children
        for index in range(len(molecule))
        if molecule[index : index + len(parent)] == parent
    }


def reverse_replacements(molecule: str, replacements: dict[str, list[str]]) -> set[str]:
    return {
        molecule[:index] + parent + molecule[index + len(child) :]
        for parent, children in replacements.items()
        for child in children
        for index in range(len(molecule))
        if molecule[index : index + len(child)] == child
    }


def insert_brackets(molecule: str) -> list[str | list]:
    molecule = molecule.join('""').join('[]')
    molecule = molecule.replace('Rn', '", [["')
    molecule = molecule.replace('Y',  '"], ["')
    molecule = molecule.replace('Ar', '"]], "')
    return json.loads(molecule)


def possible_strings(replacements, content):
    if not content:
        yield "", 0
        return
    first, *rest = content
    if isinstance(first, str):
        for possible, count in possible_strings(replacements, rest):
            yield f"{first}{possible}", count
        return
    for alternative, alt_count in resolve_brackets(first):
        for possible, pos_count in possible_strings(replacements, rest):
            yield f"{alternative}{possible}", alt_count + pos_count


def get_min_steps_to_goals(replacements, content: list[str | list], goals: set[str]) -> Iterator[tuple[str, int]]:
    print(content)
    if not content:
        yield "", 0
        return
    deja_vu = set()
    found = {}
    for possible, count in possible_strings(replacements, content):
        if possible in goals:
            if possible not in found or found[possible] > count:
                found[possible] = count
            continue
        reverses = {possible}
        sub_found = {}
        while reverses and goals != set(sub_found) and (goals != set(found) or any(val > count for val in found.values())):
            print(reverses)
            reverses = {rr for r in reverses for rr in reverse_replacements(r, replacements)} - deja_vu
            deja_vu |= reverses
            count += 1
            for r in reverses & (goals - set(sub_found)):
                sub_found[r] = count
        for key, val in sub_found.items():
            if key not in found or found[key] > val:
                found[key] = val
    yield from found.items()


def resolve_brackets(parts: list) -> Iterator[tuple[str, int]]:
    if len(parts) == 1:
        for goal, steps in get_min_steps_to_goals(replacements, parts[0], {"Al", "F", "Mg"}):
            yield f"Rn{goal}Ar", steps
        return
    if len(parts) == 2:
        for goal0, steps0 in get_min_steps_to_goals(replacements, parts[0], {"F", "Mg"}):
            for goal1, steps1 in get_min_steps_to_goals(replacements, parts[1], {"F", "Mg"}):
                if goal0 == "Mg" == goal1:
                    continue
                yield f"Rn{goal0}Y{goal1}Ar", steps0 + steps1
        return
    if len(parts) == 3:
        for goal0, steps0 in get_min_steps_to_goals(replacements, parts[0], {"F"}):
            for goal1, steps1 in get_min_steps_to_goals(replacements, parts[1], {"F"}):
                for goal2, steps2 in get_min_steps_to_goals(replacements, parts[2], {"F"}):
                    yield f"Rn{goal0}Y{goal1}Y{goal2}Ar", steps0 + steps1 + steps2
        return
    raise Exception("There were more Y than expected")







def solve(text: str) -> Iterator:
    replacements, molecule = parse(text)
    yield len(apply_replacements(molecule, replacements))

    atom_count = sum(c == c.upper() for c in molecule)
    print(atom_count - 1 - 2 * (molecule.count("Y") + molecule.count("Ar")))

    distinct = {"CRnSiRnCaPTiMgYCaPTiRnFAr"}
    while all(m.endswith("Ar") for m in distinct):
        print("|",end="")
        distinct = {mm for m in distinct for mm in reverse_replacements(m, replacements)}
    yield None




for children in replacements.values():
    for value in children:
        assert "Rn" in value or sum(c == c.upper() for c in value) == 2, value

print(molecule)
brackets = insert_brackets(molecule)
print(brackets)
atom_count = sum(c == c.upper() for c in molecule)
print(atom_count - 1 - 2 * (molecule.count("Y") + molecule.count("Ar")))
#min_steps = list(get_min_steps_to_goals(replacements, brackets, {"e"}))
#print(min_steps)

"""
Th
Ti
P
O
C
N
Si
"""
