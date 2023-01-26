"""
Advent of Code 2015 - Day 1
https://adventofcode.com/2022/day/1

Day 1: Not Quite Lisp
"""
from os.path import join as path_join
from functools import cached_property
from common import INPUT_DIR


class DailyPuzzle:
    INPUT_FILE = path_join(INPUT_DIR, 'day-01.txt')

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
        floor = 0

        for c in input:
            if c == '(':
                floor += 1
            elif c == ')':
                floor -= 1
            else:
                print(f"unexpected input: {c}")

        return floor

    @property
    def second(self):
        input = self.file_input
        floor = 0

        for n, chr in enumerate(input):
            if chr == '(':
                floor += 1
            elif chr == ')':
                floor -= 1

            if floor == -1:
                return n + 1

    #
    # Tests
    #
    @property
    def test1(self):
        input = self.TEST_INPUT
        return input

    @property
    def test2(self):
        pass

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
