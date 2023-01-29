"""
Advent of Code 2015 - Day 4
https://adventofcode.com/2015/day/4

Day 4: The Ideal Stocking Stuffer
"""
from os.path import join as path_join
from functools import cached_property
from common import INPUT_DIR

import hashlib


def santa_hash(key, target='00000'):
    n = 0
    while True:
        n += 1
        input = f"{key}{n}"
        hash = hashlib.md5(input.encode('utf-8')).hexdigest()
        if hash.startswith(target):
            return n

        print(n) if n % 100000 == 0 else None


class DailyPuzzle:
    INPUT_FILE = path_join(INPUT_DIR, 'day-04.txt')

    TEST_INPUT = """\
"""

    def solve(self):
        print(f"test 1 solution: {self.test1}")
        print(f"Part 1 Solution: {self.first}")
        print(f"test 2 solution: {self.test2}")
        print(f"Part 2 Solution: {self.second}")

    #
    # Solutions
    #
    @property
    def first(self):
        key = 'bgvyzdsv'
        answer = santa_hash(key)
        return answer

    @property
    def second(self):
        key = 'bgvyzdsv'
        answer = santa_hash(key, '000000')
        return answer

    #
    # Tests
    #
    @property
    def test1(self):
        test_cases = [
            # key, expected
            ('abcdef', 609043),
            ('pqrstuv', 1048970)
        ]

        for key, expected in test_cases:
            answer = santa_hash(key)
            assert answer == expected, (key, answer, expected)

        return 'passed'

    @property
    def test2(self):
        return 'passed'

    #
    # Properties
    #
    @cached_property
    def file_input(self):
        with open(self.INPUT_FILE) as file:
            return file.read().strip()


#
# Main
#
problem = DailyPuzzle()
problem.solve()
