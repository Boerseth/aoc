"""Corporate Policy"""
from typing import Iterator


ABC = "abcdefghijklmnopqrstuvwxyz"
ILLEGAL = set("ilo")
ABC_LEGAL = "".join(c for c in ABC if c not in ILLEGAL)

PAIRS = {c: f"{c}{c}" for c in ABC_LEGAL}
TRIOS = {a: f"{a}{b}{c}" for a, b, c in zip(ABC, ABC[1:], ABC[2:])}
# Impossible to get a run "abc" with "i", "l", "o" from "g" to "o":
#     "ghijklmno"
#        ^  ^  ^
for a in "ghijklmno":
    TRIOS[a] = TRIOS["p"]
QUINTS = {a: f"{c1}{c1}{c2}{c3}{c3}" for a, (c1, c2, c3) in TRIOS.items()}

INCREMENT = {c1: c2 for c1, c2 in zip(ABC_LEGAL, ABC_LEGAL[1:])}
INCREMENT |= {c: ABC[ABC.index(c) + 1] for c in ILLEGAL}


def increment_word(word: str) -> str:
    if word == "":
        return "a"
    *letters, last = word
    start = "".join(letters)
    if last in INCREMENT:
        return f"{start}{INCREMENT[last]}"
    return f"{increment_word(start)}a"


def bump_past_illegal(word: str) -> str:
    if not set(word) & ILLEGAL:
        return word
    first_illegal = min(word.index(char) for char in set(word) & ILLEGAL)
    start = word[:first_illegal]
    bumped = INCREMENT[word[first_illegal]]
    return f"{start}{bumped}".ljust(len(word), "a")


def get_next_pw(word: str) -> str:
    if len(word) < 5:
        return "aabcc"
    if set(word) & ILLEGAL:
        return get_next_pw(bump_past_illegal(word))

    distinct_pairs_cummulative = [set()]
    for a, b in zip(word, word[1:]):
        distinct_pairs_cummulative.append(set(distinct_pairs_cummulative[-1]))
        if a == b:
            distinct_pairs_cummulative[-1].add(a)

    contains_trio_cummulative = [False, False]
    for a, b, c in zip(word, word[1:], word[2:]):
        contains_trio_cummulative.append(contains_trio_cummulative[-1] or TRIOS.get(a) == f"{a}{b}{c}")

    if contains_trio_cummulative[-2] and len(distinct_pairs_cummulative[-2]) == 1:
        if word[-2] not in distinct_pairs_cummulative[-2] and word[-2] > word[-1]:
            return f"{word[:-2]}{word[-2]}"
        return get_next_pw(f"{increment_word(word[:-1])}a")

    if not contains_trio_cummulative[-3] and len(distinct_pairs_cummulative[-3]) == 2:
        end = word[-3:]
        if end[0] in TRIOS:
            trio = TRIOS[end[0]]
            if end < trio:
                return f"{word[:-3]}{trio}"
            return get_next_pw(f"{increment_word(word[:-2])}aa")
        return get_next_pw(f"{increment_word(word[:-3])}aaa")

    if contains_trio_cummulative[-4] and len(distinct_pairs_cummulative[-4]) == 0:
        end = word[-4:]
        if end < "zzyy":
            c1, c2, c3, c4 = end
            if c1 > c2:
                pair1 = f"{c1}{c1}"
                pair2 = "aa" if pair1 != "aa" else "bb"
                return f"{word[:-4]}{pair1}{pair2}"
            assert c1 < c2, "If the two were == it would have been caught by first if"
            return get_next_pw(f"{increment_word(word[:-3])}aaa")
        return get_next_pw(f"{increment_word(word[:-4])}aaaa")

    if not contains_trio_cummulative[-4] and len(distinct_pairs_cummulative[-4]) == 1:
        end = word[-4:]
        if end < "xyzz":
            trio = TRIOS[end[0]]
            for quad, pair in [(f"{trio[0]}{trio}", trio[0]), (f"{trio}{trio[2]}", trio[2])]:
                if quad > end and pair not in distinct_pairs_cummulative[-4]:
                    return f"{word[:-4]}{quad}"
            return get_next_pw(f"{increment_word(word[:-3])}aaa")
        return get_next_pw(f"{increment_word(word[:-4])}aaaa")

    assert not contains_trio_cummulative[-4] and len(distinct_pairs_cummulative[-4]) == 0
    assert not contains_trio_cummulative[-5] and len(distinct_pairs_cummulative[-5]) == 0

    end = word[-5:]
    if end < "xxyzz":
        quint = QUINTS[end[0]]
        if end < quint:
            return f"{word[:-5]}{quint}"
        return get_next_pw(f"{increment_word(word[:-4])}aaaa")
    return get_next_pw(f"{increment_word(word[:-5])}aaaaa")


def solve(text: str) -> Iterator[str]:
    pw = get_next_pw(text.strip())
    yield pw
    yield get_next_pw(pw)
