"""Full of Hot Air"""

SNAFU = "=-012"


def decimal_to_snafu(number):
    if number == 0:
        return "0"

    remainder = ((number + 2) % 5) - 2
    quotient = (number - remainder) // 5

    digit = SNAFU[remainder + 2]
    digits = decimal_to_snafu(quotient).lstrip("0")
    return f"{digits}{digit}"


def snafu_to_decimal(snafu):
    if not snafu:
        return 0
    return SNAFU.index(snafu[-1]) - 2 + 5 * snafu_to_decimal(snafu[:-1])


def solve(text):
    yield decimal_to_snafu(sum(map(snafu_to_decimal, text.splitlines())))
    yield None
