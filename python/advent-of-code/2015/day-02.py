"""
Advent of Code 2015 - Day 2
https://adventofcode.com/2022/day/2

Day 2: I Was Told There Would Be No Math
"""
from os.path import join as path_join
from functools import cached_property
from common import INPUT_DIR


def estimate_wrapping_paper(dims):
    l, w, h = [int(dim) for dim in dims.split('x')]
    sorted_dims = sorted([l, w, h])
    slack = sorted_dims[0] * sorted_dims[1]
    return (2*l*w) + (2*w*h) + (2*h*l) + slack


def estimate_ribbon(dims):
    l, w, h = [int(dim) for dim in dims.split('x')]
    sorted_dims = sorted([l, w, h])
    wrap = (sorted_dims[0]*2) + (sorted_dims[1]*2)
    ribbon = l*w*h
    return ribbon + wrap


class DailyPuzzle:
    INPUT_FILE = path_join(INPUT_DIR, 'day-02.txt')

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
        boxes = input.split('\n')
        sq_feet = 0

        for dims in boxes:
            sq_feet += estimate_wrapping_paper(dims)

        return sq_feet

    @property
    def second(self):
        input = self.file_input
        boxes = input.split('\n')
        feet = 0

        for dims in boxes:
            feet += estimate_ribbon(dims)

        return feet

    #
    # Tests
    #
    @property
    def test1(self):
        test_cases = [
            # input, expect
            ('2x3x4', 34),
            ('1x1x10', 14),
        ]

        for dims, expected in test_cases:
            feet = estimate_ribbon(dims)
            assert feet == expected, feet

        return 'passed'

    @property
    def test2(self):
        test_cases = [
            # input, expect
            ('2x3x4', 58),
            ('1x1x10', 43),
        ]

        for dims, expected in test_cases:
            sq_feet = estimate_wrapping_paper(dims)
            assert sq_feet == expected, sq_feet

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
