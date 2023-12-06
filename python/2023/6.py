"""Wait For It"""
from collections.abc import Iterator


def will_win(charge_time: int, total_time: int, record: int) -> bool:
    return record < charge_time * (total_time - charge_time)


def ways_to_win(time: int, record: int) -> int:
    """
    The boat's velocity will be equal to its `charge`, and it will go a distance
                charge * (time - charge)
    We want charge values that satisfy the inequality
                -(charge ** 2) + time * charge  >  record
    i.e. when the parabolic function
        f(x) =  -(charge ** 2) + time * charge - record
    changes sign. The parabola will have `center` and `width` given by
        center = time / 2
        width = sqrt(time ** 2 - 4 * record) / 2
    """
    center = time / 2
    width = max(0, time ** 2 - 4 * record) ** 0.5 / 2
    last_loss = int(center - width)
    last_win = int(center + width)
    # Account for ties and rounding errors
    last_loss = next(last_loss + dt for dt in [1, 0, -1] if not will_win(last_loss + dt, time, record))
    last_win = next(last_win + dt for dt in [1, 0, -1] if will_win(last_win + dt, time, record))
    return last_win - last_loss


def solve(text: str) -> Iterator[int]:
    lines = [line.split(":")[1] for line in text.strip().splitlines()]
    times, dists = [map(int, line.split()) for line in lines]
    time, dist = [int(line.replace(" ", "")) for line in lines]

    product = 1
    for ways in map(ways_to_win, times, dists):
        product *= ways
    yield product
    yield ways_to_win(time, dist)
