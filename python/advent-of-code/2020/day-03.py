"""
Advent of Code 2020 - Day 03
https://adventofcode.com/2020/day/3
"""
from os.path import join as path_join
from functools import cached_property
from config import INPUT_DIR

import math


INPUT_FILE = path_join(INPUT_DIR, 'day-03.txt')
TREE = '#'


class Solution:
    def __init__(self, input_file):
        self.input_file = input_file

    #
    # Properties
    #
    @property
    def first(self):
        dx = 3
        return self.traverse_map(dx, 1)

    @property
    def second(self):
        slopes = [
            (1, 1),
            (3, 1),
            (5, 1),
            (7, 1),
            (1, 2)
        ]
        trees_per_slope = []

        for dx, dy in slopes:
            trees = self.traverse_map(dx, dy)
            trees_per_slope.append(trees)

        return math.prod(trees_per_slope)

    @cached_property
    def input_lines(self):
        with open(self.input_file) as file:
            lines = file.readlines()
            return [line.strip() for line in lines]

    #
    # Methods
    #
    def map_row(self, line, x):
        mapped_row = list(line)

        if x >= len(mapped_row):
            m = x // len(mapped_row) + 1
            mapped_row *= m

        return mapped_row

    def traverse_map(self, dx, dy):
        x = 0
        map_lines = self.input_lines[dy:]
        hit_trees = 0

        # Step by dy: https://stackoverflow.com/a/2990281/1093087
        for line in map_lines[::dy]:
            x += dx
            row = self.map_row(line, x)

            if row[x] == TREE:
                hit_trees += 1

        return hit_trees


#
# Main
#
solution = Solution(INPUT_FILE)
print("pt 1 solution: {}".format(solution.first))
print("pt 2 solution: {}".format(solution.second))
