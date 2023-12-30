"""
Advent of Code 2023 - Day 15
https://adventofcode.com/2023/day/15
"""
from os.path import join as path_join
from functools import cached_property
from common import INPUT_DIR


class HolidayHash:
    def __init__(self, input):
        self.input = input.strip()

    @cached_property
    def steps(self):
        return self.input.split(',')

    @cached_property
    def sum(self):
        sum = 0
        for step in self.steps:
            hash = self.hash_value(step)
            sum += hash
        return sum

    def hash_value(self, input):
        hash = 0
        for c in list(input):
            hash += ord(c)
            hash *= 17
            hash = hash % 256
        return hash


class AdventPuzzle:
    INPUT_FILE = path_join(INPUT_DIR, 'day-15.txt')

    TEST_INPUT = """rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"""

    #
    # Solutions
    #
    @property
    def first(self):
        input = self.file_input
        hash = HolidayHash(input)
        return hash.sum

    @property
    def second(self):
        pass

    #
    # Tests
    #
    @property
    def test1(self):
        value = "HASH"
        hash = HolidayHash('')
        value = hash.hash_value(value)
        assert value == 52, value

        input = self.TEST_INPUT
        hash = HolidayHash(input)
        assert hash.sum == 1320, hash.sum
        return 'passed'

    @property
    def test2(self):
        input = self.TEST_INPUT
        hash = HolidayHash(input)
        assert hash.focusing_power == 145, hash.focusing_power
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
