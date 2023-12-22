"""
Advent of Code 2023 - Day 22
https://adventofcode.com/2023/day/22
"""
from os.path import join as path_join
from functools import cached_property
from common import INPUT_DIR


class BrickStack:
    def __init__(self, input):
        self.input = input.strip()


class Brick:
    def __init__(self, pt1, pt2):
        pass


class AdventPuzzle:
    INPUT_FILE = path_join(INPUT_DIR, 'day-22.txt')

    TEST_INPUT = """\
"""

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
        input = self.TEST_INPUT
        stack = BrickStack(input)
        assert stack.safe_bricks == 5, stack.safe_bricks
        return 'passed'

    @property
    def test2(self):
        input = self.TEST_INPUT
        print(input)
        return 'passed'

    #
    # Etc...
    #
    @cached_property
    def file_input(self):
        with open(self.INPUT_FILE) as file:
            return file.read().strip()

    def solve(self):
        print(f"test 1 solution: {self.test1}")
        print(f"Part 1 Solution: {self.first}")
        print(f"test 2 solution: {self.test2}")
        print(f"Part 2 Solution: {self.second}")


#
# Main
#
puzzle = AdventPuzzle()
puzzle.solve()
