"""
Advent of Code 2021 - Day 14
https://adventofcode.com/2021/day/14
"""
from os.path import join as path_join
from functools import cached_property
from config import INPUT_DIR


INPUT_FILE = path_join(INPUT_DIR, 'day-14.txt')
POLYMER_TEMPLATE = 'CNBPHFBOPCSPKOFNHVKV'


class Solution:
    def __init__(self, input_file):
        self.input_file = input_file

    #
    # Solutions
    #
    @staticmethod
    def first():
        solution = Solution(INPUT_FILE)

    @staticmethod
    def second():
        solution = Solution(INPUT_FILE)

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
print("pt 1 solution: {}".format(Solution.first()))
print("pt 2 solution: {}".format(Solution.second()))
