"""JSAbacusFramework.io"""
import json
from typing import Iterator


JSON = int | dict[str, "JSON"], list["JSON"]


def sum_numbers(json_structure: JSON) -> complex:
    """Real part is naive sum; Imag part is part of sum tainted by "red" values"""
    if isinstance(json_structure, int):
        return complex(json_structure, 0)
    if isinstance(json_structure, list):
        return sum(sum_numbers(item) for item in json_structure)
    if isinstance(json_structure, dict):
        values = list(json_structure.values())
        result = sum_numbers(values)
        return complex(result.real, result.real if "red" in values else result.imag)
    return 0


def solve(text: str) -> Iterator[int]:
    json_structure = json.loads(text)
    result = sum_numbers(json_structure)
    yield int(result.real)
    yield int(result.real - result.imag)
