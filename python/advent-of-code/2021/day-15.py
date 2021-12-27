"""
Advent of Code 2021 - Day 15
https://adventofcode.com/2021/day/15
"""
from os.path import join as path_join
from functools import cached_property
from config import INPUT_DIR


INPUT_FILE = path_join(INPUT_DIR, 'day-15.txt')


class Solution:
    #
    # Solutions
    #
    @staticmethod
    def test():
        pass

    @staticmethod
    def first():
        pass

    @staticmethod
    def second():
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
    def __init__(self, input_file):
        self.input_file = input_file

#
# Main
#
print("test: {}".format(Solution.test()))
print("pt 1 solution: {}".format(Solution.first()))
print("pt 2 solution: {}".format(Solution.second()))
