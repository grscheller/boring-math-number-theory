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

from boring_math.number_theory import jacobi_symbol, legendre_symbol

class Test_symbols:
    def test_symbols(self) -> None:
        legendre3 = [0, 1, -1, 0, 1, -1, 0, 1, -1]
        for ii in range(9):
            assert legendre_symbol(ii, 3) == jacobi_symbol(ii, 3) == legendre3[ii]

        legendre5 = [0, 1, -1, -1, 1, 0, 1, -1, -1, 1]
        for ii in range(10):
            assert legendre_symbol(ii, 5) == jacobi_symbol(ii, 5) == legendre5[ii]

        legendre127 = [0, 1, 1, -1, 1, -1, -1, -1,  1,  1, -1, 1, -1,  1, -1,
                       1, 1, 1,  1, 1, -1,  1,  1, -1, -1,  1, 1, -1, -1, -1, 1]
        for ii in range(31):
            assert legendre_symbol(ii, 127) == jacobi_symbol(ii, 127) == legendre127[ii]

        jacobi1 = [1] * 100
        for ii in range(100):
            assert jacobi_symbol(ii, 1) == jacobi1[ii] == 1

        jacobi7 =[0, 1, 1, -1, 1, -1, -1, 0, 1, 1, -1, 1, -1, -1]
        for ii in range(14):
            assert jacobi_symbol(ii, 7) == jacobi7[ii]

        jacobi15 = [0, 1, 1, 0, 1, 0, 0, -1, 1, 0, 0, -1, 0, -1, -1,
                    0, 1, 1, 0, 1, 0, 0, -1, 1, 0, 0, -1, 0, -1, -1]
        for ii in range(30):
            assert jacobi_symbol(ii, 15) == jacobi15[ii]
