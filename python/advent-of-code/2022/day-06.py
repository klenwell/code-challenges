"""
Advent of Code 2022 - Day 6
https://adventofcode.com/2022/day/6
"""
from os.path import join as path_join
from functools import cached_property
from config import INPUT_DIR


INPUT_FILE = path_join(INPUT_DIR, 'day-06.txt')


class Solution:
    def __init__(self, input_file):
        self.input_file = input_file

    #
    # Solutions
    #
    @property
    def first(self):
        input = self.input_lines[0]
        return self.detect_message_marker(input, 4)

    @property
    def second(self):
        input = self.input_lines[0]
        return self.detect_message_marker(input, 14)

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
    def detect_message_marker(self, input, marker_len):
        for n in range(len(input)):
            word = input[n:n+marker_len]

            if len(set(word)) == marker_len:
                return n + marker_len


#
# Main
#
solution = Solution(INPUT_FILE)
print("pt 1 solution: {}".format(solution.first))
print("pt 2 solution: {}".format(solution.second))
