"""
Advent of Code 2021 - Day 08
https://adventofcode.com/2021/day/8
"""
from os.path import join as path_join
from functools import cached_property
from config import INPUT_DIR


INPUT_FILE = path_join(INPUT_DIR, 'day-08.txt')


class Solution:
    def __init__(self, input_file):
        self.input_file = input_file

    #
    # Properties
    #
    @property
    def first(self):
        pass

    @property
    def second(self):
        pass

    @cached_property
    def input_lines(self):
        with open(self.input_file) as file:
            lines = file.readlines()
            return [line.strip() for line in lines]

    #
    # Methods
    #


#
# Main
#
solution = Solution(INPUT_FILE)
print("pt 1 solution: {}".format(solution.first))
print("pt 2 solution: {}".format(solution.second))
