"""Doesn't He Have Intern-Elves For This?"""

def is_nice_1(s):
    if not 3 <= sum(1 for c in s if c in "aeiou"):
        return False
    if not any(a == b for a, b in zip(s, s[1:])):
        return False
    if any(banned in s for banned in ["ab", "cd", "pq", "xy"]):
        return False
    return True


def is_nice_2(s):
    if not any(a == b for a, b in zip(s, s[2:])):
        return False
    if not any(s[i:i+2] in s[i+2:] for i in range(len(s) - 2)):
        return False
    return True


def solve(text):
    text = text.splitlines()
    yield len(list(filter(is_nice_1, text)))
    yield len(list(filter(is_nice_2, text)))
