"""Medicine for Rudolph"""
import json
from typing import Iterator


Rules = dict[str, list[str]]


def parse(text: str) -> tuple[Rules, str]:
    rules, molecule = text.split("\n\n")
    lookup = {}
    for rule in rules.strip().splitlines():
        start, _, end = rule.split()
        lookup.setdefault(start, list()).append(end)
    return lookup, molecule.strip()


def decay(molecule: str, rules: Rules) -> set[str]:
    return {
        molecule[:index] + child + molecule[index + len(parent) :]
        for parent, children in rules.items()
        for child in children
        for index in range(len(molecule))
        if molecule[index : index + len(parent)] == parent
    }


def solve(text: str) -> Iterator:
    rules, molecule = parse(text)
    yield len(decay(molecule, rules))

    """
    Rules are either of the form
        Aa => BbCc    (1 to 2 elements)
    or
        Aa => BbRnCcAr
                ^   ^
        Aa => BbRnCcYDdAr
                ^   ^  ^
        Aa => BbRnCcYDdYEeAr
                ^   ^  ^  ^
    Note that  Rn,Y,Ar  do not decay ever.

    We can therefore compute the number of decays by counting the number of
    atoms in the molecule, and the number of  Rn,Y,Ar  atoms
    """

    assert "Rn" not in rules
    assert "Y" not in rules
    assert "Ar" not in rules
    for children in rules.values():
        for child in children:
            count_els = sum(c == c.upper() for c in child)
            count_rn = child.count("Rn")
            count_y = child.count("Y")
            count_ar = child.count("Ar")
            contains_speciel_elements = any([count_rn, count_y, count_ar])

            child_is_regular = (not contains_speciel_elements) and count_els == 2
            child_is_special = count_rn == count_ar == 1 and count_els == 2 * (1 + count_y + 1)

            assert child_is_regular or child_is_special

    atom_count = sum(c == c.upper() for c in molecule)
    y_count = molecule.count("Y")
    ar_count = molecule.count("Ar")
    assert molecule.count("Rn") == ar_count

    yield atom_count - 2 * (y_count + ar_count) - 1
