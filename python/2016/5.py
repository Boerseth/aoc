"""How About a Nice Game of Chess?"""
from hashlib import md5
from typing import Iterator


def find_password(door_id: str) -> str:
    password = ""
    goal = "00000"
    i = -1
    while len(password) < 8:
        i += 1
        door_hash = md5(f"{door_id}{i}".encode()).hexdigest()
        if door_hash.startswith(goal):
            password += door_hash[len(goal)]
    return password


def find_password_2(door_id: str) -> str:
    digits = {}
    goal = "00000"
    i = -1
    while len(digits) < 8:
        i += 1
        door_hash = md5(f"{door_id}{i}".encode()).hexdigest()
        if not door_hash.startswith(goal):
            continue
        position = door_hash[5]
        if position > "7" or position in digits:
            continue
        digits[door_hash[5]] = door_hash[6]
    return "".join(digits[f"{i}"] for i in range(8))


# def assert_equal(a, b):
#     assert a == b, (a, b)
# test_pw_2 = "".join(digit for _, digit in sorted(find_password_2("abc").items()))
# assert_equal(test_pw_2, "05ace8e3")
# assert_equal(find_password("abc"), "18f47a30")


def solve(text: str) -> Iterator:
    yield find_password(text.strip())
    yield find_password_2(text.strip())
