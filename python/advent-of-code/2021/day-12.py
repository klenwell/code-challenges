"""
Advent of Code 2021 - Day 12
https://adventofcode.com/2021/day/12
"""
from os.path import join as path_join
from functools import cached_property
from config import INPUT_DIR


DAY_NUM = 12
FNAME = 'day-{:02d}.txt'.format(DAY_NUM)
INPUT_FILE = path_join(INPUT_DIR, FNAME)


class Solution:
    def __init__(self, input_file):
        self.input_file = input_file

    #
    # Solutions
    #
    @property
    def first(self):
        pass

    @property
    def second(self):
        pass

    #
    # Properties
    #
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
