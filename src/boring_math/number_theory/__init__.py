# Copyright 2016-2025 Geoffrey R. Scheller
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
.. admonition:: Elementary Number Theory

    Collection of integer related functions useful in number theory.

    - elementary functions

      - **gcd(m, n)**: find greatest common denominator of m and n
      - **lcm(m, n)**: find least common multiple of m and n
      - **coprime(m, n)**: return tuple without common factors, preserve signs
      - **iSqrt(n)**: find unique m such that m*m <= n < (m+1)*(m+1)
      - **isSqr(n)**: true if n is a perfect square

    - symbols

      - **legendre_symbol(a, p)**: Legendre symbol (a/p) ∈ {-1, 0, 1} where p odd prime
      - **jacobi_symbol(a, n)**: Jacobi symbol (a/n) ∈ {-1, 0, 1} where n positive odd integer

    - prime functions & generators

      - **is_prime(n)**: true if n is a prime number
      - **primes(n, m)**: generate primes n <= p <= m where m is optional

"""

from collections.abc import Iterator
from typing import cast, Final
from pythonic_fp.circulararray.auto import CA
from pythonic_fp.iterables.folding import fold_left

__all__ = [
    'gcd',
    'lcm',
    'coprime',
    'iSqrt',
    'isSqr',
    'is_prime',
    'legendre_symbol',
    'jacobi_symbol',
    'primes',
    'primes_capped',
    'primes_wilson',
]


def gcd(m: int, n: int, /) -> int:
    """
    .. admonition:: gcd - greatest common divisor

        Uses Euclidean algorithm to compute the gcd of two integers.

        :param m: First int for gcd calculation.
        :param n: Second int for gcd calculation.
        :returns: The gcd of the absolute values of m and n.

        .. note::

            - mathematically the gcd(0, 0) does not exist

              - taking gcd(0, 0) = 1

                - Better choice than math.gcd(0, 0) = 0.
                - More mathematically justified.
                - Eliminates lcm & coprime having to edge case test.

    """
    if 0 == m == n:
        return 1
    m, n = abs(m), abs(n)
    while n > 0:
        m, n = n, m % n
    return m


def lcm(m: int, n: int, /) -> int:
    """
    .. admonition:: lcm - least common multiple

        Find the least common multiple (lcm) of two integers.

        :param m: First int for lcm calculation.
        :param n: Second int for lcm calculation.
        :returns: The lcm of the absolute values of m and n.

    """
    m //= gcd(m, n)
    return abs(m * n)


def coprime(m: int, n: int, /) -> tuple[int, int]:
    """
    .. admonition:: coprime

        Make 2 integers coprime by dividing out their common factors.

        :param m: First int for coprime calculation.
        :param n: Second int for coprime calculation.
        :returns: Coprimed values with original signs,
                  also (0, 0) when n = m = 0.

    """
    common = gcd(m, n)
    return m // common, n // common


def iSqrt(n: int, /) -> int:
    """
    .. admonition:: iSqrt - integer square root

        Takes the integer square root of a non-negative integer.

        :param n: Integer whose integer square root is to be found.
        :returns: The unique m such that m*m <= n < (m+1)*(m+1)
        :raises ValueError: if n < 0.

    """
    if n < 0:
        msg = 'iSqrt(n): n must be non-negative'
        raise ValueError(msg)
    high = n
    low = 1
    while high > low:
        high = (high + low) // 2
        low = n // high
    return high


def isSqr(n: int, /) -> bool:
    """
    .. admonition:: isSqr

        Determine if argument is a perfect square.

        :param n: Integer to check.
        :returns: True only if integer argument is a perfect square.

    """
    return False if n < 0 else n == iSqrt(n) ** 2


def legendre_symbol(a: int, p: int) -> int:
    """
    .. admonition:: Legendre symbol

        Calculate the Legendre Symbol (a/p) where p is an odd prime.

        :param a: any integer
        :param p: any prime ``p > 2``, does not check that ``p`` is actually prime
        :returns: the Legendre Symbol ``(a/p) ∈ {-1, 0, 1}``
        :raises ValueError: if ``abs(p) < 3``

        .. note::

            See https://en.wikipedia.org/wiki/Legendre_symbol

    """
    p = abs(p)
    if p < 3:
        msg = 'p must be a prime greater than 2'
        raise ValueError(msg)
    a = a % p

    if a == 0:
        return 0
    else:
        for x in range(1, p):
            if x * x % p == a:
                return 1
        return -1


def jacobi_symbol(a: int, n: int) -> int:
    """
    .. admonition:: Jacobi symbol

        Calculate the Jacobi symbol (a/n) where n is a positive odd integer.

        :param a: Any integer.
        :param n: Any positive odd integer.
        :returns: The Jacobi Symbol (a/n) ∈ {-1, 0, 1}.
        :raises ValueError: If n is not a positive odd integer.

        .. note::

            See https://en.wikipedia.org/wiki/Jacobi_symbol

    """
    if n <= 0 or n % 2 == 0:
        msg = 'n must be a positive odd integer'
        raise ValueError(msg)

    a = a % n
    t = 1
    while a != 0:
        while a % 2 == 0:
            a = a // 2
            r = n % 8
            if r == 3 or r == 5:
                t = -t
        n, a = a, n
        if n % 4 == 3 and a % 4 == 3:
            t = -t
        a = a % n

    if n == 1:
        return t
    else:
        return 0


def primes_wilson(start: int = 2) -> Iterator[int]:
    """
    .. admonition:: primes via Wilson's theorem

        Prime number generation using Wilson's Theorem.

        :param start: First value to check, defaults to 2.
        :yields: Prime numbers tarting from n.

        .. note::

            **Wilson's Theorem:**
            ``∀(n>1) n is prime if and only if (n-1)! % n ≡ -1``

    """
    if start < 2:
        n = 2
        fact = 1
    else:
        n = start
        fact = CA(range(2, n)).foldl(lambda j, k: j * k, 1)
    while True:
        if fact % n == n - 1:
            yield n
        fact *= n
        n += 1


def primes_capped(start: int, end: int) -> Iterator[int]:
    """
    .. admonition:: primes capped

        Generate all primes ``start <= p <= end``.

        :param start: First value to check.
        :param start: Last value to check.
        :yields: All primes p where ``start <= p <= end``.

    """
    for ii in primes_wilson(start):
        if ii < end:
            yield ii
        elif ii == end:
            yield ii
            break
        else:
            break


def primes(start: int = 2, end: int | None = None) -> Iterator[int]:
    """
    .. admonition:: primes

        Generate all primes p where start <= p <= end.

        :param start: First value to check, defaults to 2.
        :param end: Optional last value to check.
        :yields: All primes between start and end inclusive.

        .. warning::

            If end is not given, returned iterator is infinite.

    """
    if end is None:
        return primes_wilson(start)
    else:
        return primes_capped(start, end)


_prod13: Final[int] = 2 * 3 * 5 * 7 * 11 * 13
_prod17: Final[int] = _prod13 * 17
_prod19: Final[int] = _prod17 * 19
_prod23: Final[int] = _prod19 * 23
_fact13: int | None = None
_fact17: int | None = None
_fact19: int | None = None
_fact23: int | None = None

def is_prime(n: int, /) -> bool:
    """
    .. admonition:: is prime

        Test if argument is a prime number, uses Wilson's Theorem.

        :param n: Integer to check if prime.
        :returns: True only if n is prime.

    """
    global _fact13
    global _fact17
    global _fact19
    global _fact23

    def mult(j: int, k: int) -> int:
        return j * k

    if (n := abs(n)) < 2:
        return False

    if n > 23 and gcd(n, _prod23) > 1:
        return False

    if n >= _prod13:
        if _fact13 is None:
            _fact13 = fold_left(range(2, _prod13 + 1), mult, 1)
        if n >= _prod17:
            if _fact17 is None:
                _fact17 = fold_left(range(_prod13 + 1, _prod17 + 1), mult, _fact13)
            if n >= _prod19:
                if _fact19 is None:
                    _fact19 = fold_left(range(_prod17 + 1, _prod19 + 1), mult, _fact17)
                if n >= _prod23:
                    if _fact23 is None:
                        _fact23 = fold_left(range(_prod19 + 1, _prod23 + 1), mult, _fact19)

    if n < _prod13:
        return fold_left(range(2, n), mult, 1) % n == n - 1
    elif n < _prod17:
        return fold_left(range(_prod13 + 1, n), mult, cast(int, _fact13)) % n == n - 1
    elif n < _prod19:
        return fold_left(range(_prod17 + 1, n), mult, cast(int, _fact17)) % n == n - 1
    elif n < _prod23:
        return fold_left(range(_prod19 + 1, n), mult, cast(int, _fact19)) % n == n - 1
    else:
        return fold_left(range(_prod23 + 1, n), mult, cast(int, _fact23)) % n == n - 1

