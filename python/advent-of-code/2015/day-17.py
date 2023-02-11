"""
Advent of Code 2015 - Day 17
https://adventofcode.com/2015/day/17
"""
from os.path import join as path_join
from functools import cached_property
from common import INPUT_DIR


def subset_sum(array, num):
    result = []
    def find(arr, num, path=()):
        if not arr:
            return
        if arr[0] == num:
            result.append(path + (arr[0],))
        else:
            find(arr[1:], num - arr[0], path + (arr[0],))
        find(arr[1:], num, path)
    find(array, num)
    return result


class AdventPuzzle:
    INPUT_FILE = path_join(INPUT_DIR, 'day-17.txt')

    TEST_INPUT = """\
20
15
10
5
5"""

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
        target = 25
        input = self.TEST_INPUT
        array = [int(n) for n in input.split('\n')]
        subsets = subset_sum(array, target)
        assert len(subsets) == 4, subsets
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
puzzle = AdventPuzzle()
puzzle.solve()
