"""
Advent of Code 2022 - Day 3
https://adventofcode.com/2022/day/3

References:
https://www.pythontutorial.net/python-basics/python-set-intersection/

"""
from os.path import join as path_join
from functools import cached_property
from config import INPUT_DIR
import string


INPUT_FILE = path_join(INPUT_DIR, 'day-03.txt')


class Solution:
    def __init__(self, input_file):
        self.input_file = input_file

    #
    # Solutions
    #
    @property
    def first(self):
        sum = 0
        for line in self.input_lines:
            part1, part2 = self.split_sack(line)
            common_item = list(set(part1).intersection(part2))[0]
            value = self.prioritize(common_item)
            sum += value
        return sum

    @property
    def second(self):
        sum = 0
        step = 3

        # https://www.geeksforgeeks.org/break-list-chunks-size-n-python/
        # Isn't there an itertool that does this?
        for i in range(0, len(self.input_lines), step):
            x = i
            ruck1, ruck2, ruck3 = self.input_lines[x:x+step]
            badge = list(set(ruck1) & set(ruck2) & set(ruck3))[0]
            value = self.prioritize(badge)
            sum += value

        return sum

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
    def split_sack(self, line):
        line_len = len(line)
        half = int(line_len / 2)
        return line[:half], line[half:]

    def prioritize(self, item):
        # https://stackoverflow.com/a/3190207/1093087
        priorities = list(string.ascii_lowercase)

        idx = item.lower()
        value = priorities.index(idx) + 1

        if item.isupper():
            value += 26

        return value


#
# Main
#
solution = Solution(INPUT_FILE)
print("pt 1 solution: {}".format(solution.first))
print("pt 2 solution: {}".format(solution.second))
