"""Infinite Elves and Infinite Houses"""
import math
from typing import Iterator



gamma = 0.57721566490153286060651209008240243104215933593992
exp_gamma = math.exp(gamma)


class PrimeGenerator:
    def __init__(self):
        self._found_primes = [2, 3, 5, 7]

    def _is_prime(self, number: int) -> bool:
        return all(number % p for p in self.get_primes(number ** 0.5))

    def get_primes(self, upper: int | float) -> Iterator[int]:
        for p in self._found_primes:
            if p > upper:
                return
            yield p
        if self._found_primes[-1] >= upper:
            return
        for p in range(self._found_primes[-1] + 2, int(upper) + 1, 2):
            if self._is_prime(p):
                self._found_primes.append(p)
                yield p

    def get_prime_factors(self, number: int) -> Iterator[tuple[int, int]]:
        for p in self.get_primes(number ** 0.5):
            if number % p:
                continue

            multiplicity = 0
            while not number % p:
                number //= p
                multiplicity += 1
            yield p, multiplicity
            if not number:
                break
        if number != 1:
            yield number, 1

    def sigma(self, number: int) -> int:
        sigma = 1
        for p, mult in self.get_prime_factors(number):
            sigma *= (p ** (mult + 1) - 1) // (p - 1)
        assert sigma < self.sigma_upper_bound(number), number
        return sigma

    def sigma_upper_bound(self, n: int) -> float:
        if n < 3:
            return 4
        loglog_n = math.log(math.log(n))
        if n <= 5040:
            return exp_gamma * n * loglog_n + 0.6483 * n / loglog_n
        return exp_gamma * n * loglog_n  # Let us assume that the Riemann hypothesis is true

    def get_divisors(self, n: int, upper_bound: int = None) -> list[int]:
        upper_bound = upper_bound or n
        yield 1
        divisors = [1]
        for p, mult in self.get_prime_factors(min(n, upper_bound)):
            new_divisors = []
            for m in range(mult):
                factor = p ** (m + 1)
                if factor > upper_bound:
                    break
                for d in divisors:
                    new_divisor = d * factor
                    if new_divisor > upper_bound:
                        break
                    new_divisors.append(new_divisor)
            yield from new_divisors
            divisors.extend(new_divisors)

    def visits(self, house: int) -> int:
        return sum(self.get_divisors(house, 50))


def compute_sum_of_divisors(factors: list[tuple[int, int]]) -> int:
    sigma = 1
    for p, mult in factors:
        sigma *= (p ** (mult + 1) - 1) // (p - 1)
    return sigma


def visits(house: int) -> int:
    return sum(house // divisor for divisor in range(1, min(51, house)) if not house % divisor)


def solve(text: str) -> Iterator[int]:
    goal = int(text)
    generator = PrimeGenerator()

    """
    We seek an  n  such that  goal < sigma(n) .
    But for  n > 3  it is known that
        sigma(n)  <  e**(gamma) * log(log(n))  +  0.6483n / log(log(n))
    So if we find the first  n  such that
        goal  <  e**(gamma) * log(log(n))  +  0.6483n / log(log(n))
    then  n - 1  will be the best place to start looking!
    """

    house = 1
    # Starting point: find a number that satisfies Ramanujan/Robin inequality:
    while goal > 10 * generator.sigma_upper_bound(house):
        house += 1
    while goal > 10 * generator.sigma(house):
        house += 1
    yield house

    house = 1
    while goal > 11 * visits(house):
        house += 1
    yield house
