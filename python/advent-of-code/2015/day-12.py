"""
Advent of Code 2015 - Day 12
https://adventofcode.com/2015/day/12

Day 12: JSAbacusFramework.io
"""
from os.path import join as path_join
from functools import cached_property
from common import INPUT_DIR, extract_numbers


class ElfAcctFile:
    def __init__(self, input):
        self.input = input.strip()

    @cached_property
    def sum(self):
        return sum(self.numbers)

    @cached_property
    def numbers(self):
        return extract_numbers(self.input, num_type=int)



class DailyPuzzle:
    INPUT_FILE = path_join(INPUT_DIR, 'day-12.txt')

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
        input = self.file_input
        return input

    @property
    def second(self):
        pass

    #
    # Tests
    #
    @property
    def test1(self):
        test_cases = [
            # input, sum
            ('[1,2,3]', 6),
            ('{"a":2,"b":4}', 6),
            ('[[[3]]]', 3),
            ('{"a":{"b":4},"c":-1}', 3),
            ('{"a":[-1,1]}', 0),
            ('[-1,{"a":1}]', 0),
            ('[]', 0),
            ('{}', 0),
        ]

        for input, expected in test_cases:
            acct_file = ElfAcctFile(input)
            assert acct_file.sum == expected, (input, acct_file.sum, expected)

        return 'passed'

    @property
    def test2(self):
        input = self.TEST_INPUT
        print(input)
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
