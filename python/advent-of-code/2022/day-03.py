"""
Advent of Code 2022 - Day 3
https://adventofcode.com/2022/day/3
"""
from os.path import join as path_join
from functools import cached_property
from config import INPUT_DIR


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
            ruck1, ruck2 = self.split_sack(line)
            common_item = list(set(ruck1).intersection(ruck2))[0]
            print(line, ruck1, ruck2, common_item)
            value = self.prioritize(common_item)
            print(common_item, value)
            sum += value
        return sum

    def split_sack(self, line):
        line_len = len(line)
        half = int(line_len / 2)
        return line[:half], line[half:]

    def prioritize(self, item):
        import string
        priority_map = list(string.ascii_lowercase)

        idx = item.lower()
        value = priority_map.index(idx) + 1

        if item.isupper():
            value += 26
        return value


    @property
    def second(self):
        sum = 0
        step = 3

        for i in range(0, len(self.input_lines), step):
            x = i
            ruck1, ruck2, ruck3 = self.input_lines[x:x+step]
            badge = list(set(ruck1) & set(ruck2) & set(ruck3))[0]
            print(ruck1, ruck2, badge)
            value = self.prioritize(badge)
            print(badge, value)
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


#
# Main
#
solution = Solution(INPUT_FILE)
print("pt 1 solution: {}".format(solution.first))
print("pt 2 solution: {}".format(solution.second))
