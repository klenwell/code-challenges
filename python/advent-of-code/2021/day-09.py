"""
Advent of Code 2021 - Day 09
https://adventofcode.com/2021/day/9
"""
from os.path import join as path_join
from functools import cached_property
from config import INPUT_DIR


INPUT_FILE = path_join(INPUT_DIR, 'day-09.txt')


class Solution:
    def __init__(self, input_file):
        self.input_file = input_file

    #
    # Properties
    #
    @property
    def first(self):
        risk_level = 0

        for x in range(self.row_count):
            for y in range(self.column_count):
                if self.is_low_point(x, y):
                    risk = self.grid[(x, y)]
                    print(x, y, risk)
                    risk_level += risk + 1

        return risk_level

    @property
    def second(self):
        pass

    @cached_property
    def input_lines(self):
        with open(self.input_file) as file:
            lines = file.readlines()
            return [line.strip() for line in lines]

    @cached_property
    def grid(self):
        grid_map = {}
        for x, line in enumerate(self.input_lines):
            cols = list(line)
            for y, val in enumerate(cols):
                grid_map[(x, y)] = int(val)
        return grid_map

    @cached_property
    def row_count(self):
        return len(self.input_lines)

    @cached_property
    def column_count(self):
        return len(self.input_lines[0])

    #
    # Methods
    #
    def is_low_point(self, x, y):
        default_value = 100

        pt = self.grid[(x, y)]
        n = self.grid.get((x, y-1), default_value)
        s = self.grid.get((x, y+1), default_value)
        e = self.grid.get((x+1, y), default_value)
        w = self.grid.get((x-1, y), default_value)

        for dir in (n, s, e, w):
            if pt >= dir:
                return False

        return True


#
# Main
#
solution = Solution(INPUT_FILE)
print("pt 1 solution: {}".format(solution.first))
print("pt 2 solution: {}".format(solution.second))
