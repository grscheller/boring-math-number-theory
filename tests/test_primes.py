# Copyright 2023-2024 Geoffrey R. Scheller
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

from boring_math.number_theory import is_prime, primes_wilson, primes

class Test_primes:
    def test_primes(self) -> None:
        assert len(list(primes(10, 5))) == 0
        assert len(list(primes(11, 5))) == 0
        assert len(list(primes(end=11))) == 5
        assert len(list(primes(end=12))) == 5
        assert len(list(primes(start=5, end=11))) == 3
        assert len(list(primes(start=4, end=12))) == 3

        cnt = 0
        primeList: list[int] = []
        for kk in primes_wilson(36):
            cnt += 1
            if cnt > 5:
                assert False
            primeList.append(kk)
            if kk >= 53:
                break
        assert primeList == [37, 41, 43, 47, 53]

        cnt = 0
        primeList = []
        for kk in primes(36):
            cnt += 1
            if cnt > 5:
                assert False
            primeList.append(kk)
            if kk >= 53:
                break
        assert primeList == [37, 41, 43, 47, 53]

        generated = list(primes(10, 50))
        assert generated == [11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
        generated = list(primes(10, 8))
        assert generated == []
        generated = list(primes(0, 3))
        assert generated == [2, 3]
        generated = list(primes(-5, 4))
        assert generated == [2, 3]

    def test_is_prime(self) -> None:
        assert not is_prime(0)
        assert not is_prime(1)
        assert is_prime(2)
        assert is_prime(3)
        assert not is_prime(4)
        assert is_prime(5)
        assert not is_prime(6)
        assert is_prime(7)
        assert not is_prime(100)
        assert is_prime(101)
        assert not is_prime(111)
        assert is_prime(2309)
        assert is_prime(2311)
        assert not is_prime(11111)
        assert is_prime(11113)
        assert is_prime(22229)
        assert is_prime(30029)
        assert is_prime(30103)
        assert not is_prime(35369)
        assert not is_prime(188921)
        assert not is_prime(233411)
#       assert is_prime(510457)
#       assert is_prime(510611)
#       assert not is_prime(111111111111111111)
#       assert is_prime(1111111111111111111)
#       assert not is_prime(11111111111111111111)
