"""
Advent of Code 2022 - Day 25
https://adventofcode.com/2022/day/25
"""
from os.path import join as path_join
from functools import cached_property
from config import INPUT_DIR


INPUT_FILE = path_join(INPUT_DIR, 'day-25.txt')

TEST_INPUT = """\
1=-0-2
12111
2=0=
21
2=01
111
20012
112
1=-1=
1-12
12
1=
122"""


class SnafuNumber:
    DECIMAL_MAP = {
        '2': 2,
        '1': 1,
        '0': 0,
        '-': -1,
        '=': -2
    }

    @staticmethod
    def from_dec(n):
        digits = []
        int_snafu_map = {v: k for k, v in SnafuNumber.DECIMAL_MAP.items()}
        carry_over = 0

        while n or carry_over > 0:
            b5_digit = n % 5
            b5_digit = b5_digit + 1 if carry_over else b5_digit
            carry_over = 0
            if b5_digit > 2:
                carry_over = 1
                b5_digit -= 5
                b5_digit = 0 if b5_digit == -5 else b5_digit
            b5_chr = int_snafu_map[b5_digit]
            digits.insert(0, b5_chr)
            n = n // 5

        return ''.join(digits)

    def __init__(self, input):
        self.input = input

    @cached_property
    def digits(self):
        return list(reversed(self.input))

    @cached_property
    def decimal(self):
        output = 0
        for n, digit in enumerate(self.digits):
            int = SnafuNumber.DECIMAL_MAP[digit]
            output += 5**n * int
        return output

    def __add__(self, other):
        places = max(len(self.input), len(other.input))
        return

class Solution:
    def __init__(self, input_file):
        self.input_file = input_file

    #
    # Solutions
    #
    @property
    def test1(self):
        test_cases = [
            # Decimal, SNAFU
            (1, '1'),
            (4, '1-'),
            (10, '20'),
            (314159265, '1121-1110-1=0')
        ]

        for dec, snafu in test_cases:
            dec_to_snafu = SnafuNumber(snafu).decimal
            snafu_to_dec = SnafuNumber.from_dec(dec)
            assert dec_to_snafu == dec, (dec_to_snafu, snafu, dec)
            assert snafu_to_dec == snafu, (snafu_to_dec, dec, snafu)

        sum = 0
        for n in self.test_input_lines:
            sum += SnafuNumber(n).decimal
        snafu_sum = SnafuNumber.from_dec(sum)

        assert sum == 4890, sum
        assert snafu_sum == '2=-1=0', snafu_sum
        return snafu_sum

    @property
    def first(self):
        sum = 0
        for n in self.input_lines:
            print(n)
            sum += SnafuNumber(n).decimal
        return SnafuNumber.from_dec(sum)

    @property
    def test2(self):
        pass

    @property
    def second(self):
        pass

    #
    # Properties
    #
    @cached_property
    def file_input(self):
        with open(self.input_file) as file:
            return file.read().strip()

    @cached_property
    def input_lines(self):
        return [line.strip() for line in self.file_input.split("\n")]

    @cached_property
    def test_input_lines(self):
        return [line.strip() for line in TEST_INPUT.split("\n")]

    #
    # Methods
    #


#
# Main
#
solution = Solution(INPUT_FILE)
print("test 1 solution: {}".format(solution.test1))
print("pt 1 solution: {}".format(solution.first))
print("test 2 solution: {}".format(solution.test2))
print("pt 2 solution: {}".format(solution.second))
