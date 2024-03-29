"""
Advent of Code 2022 - Day 4
https://adventofcode.com/2022/day/4

References:

"""
from os.path import join as path_join
from functools import cached_property
from config import INPUT_DIR


INPUT_FILE = path_join(INPUT_DIR, 'day-04.txt')


class Solution:
    def __init__(self, input_file):
        self.input_file = input_file

    #
    # Solutions
    #
    @property
    def first(self):
        redundancies = []
        for line in self.input_lines:
            sec1, sec2 = line.split(',')
            if self.section_contains_other(sec1, sec2):
                redundancies.append((sec1, sec2))
        return len(redundancies)

    @property
    def second(self):
        overlaps = []

        for line in self.input_lines:
            sec1, sec2 = line.split(',')
            start1, end1 = sec1.split('-')
            start2, end2 = sec2.split('-')

            set1 = set(range(int(start1), int(end1)+1))
            set2 = set(range(int(start2), int(end2)+1))
            overlapping_sections = list(set1.intersection(set2))

            if len(overlapping_sections) > 0:
                overlaps.append(overlapping_sections)

        return len(overlaps)

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
    def section_contains_other(self, sec1, sec2):
        start1, end1 = sec1.split('-')
        start2, end2 = sec2.split('-')

        if int(start1) <= int(start2) and int(end1) >= int(end2):
            return True

        if int(start2) <= int(start1) and int(end2) >= int(end1):
            return True

        return False


#
# Main
#
solution = Solution(INPUT_FILE)
print("pt 1 solution: {}".format(solution.first))
print("pt 2 solution: {}".format(solution.second))
