"""
Advent of Code 2020 - Day 6
https://adventofcode.com/2021/day/6
"""
from os.path import join as path_join
from functools import cached_property
from config import INPUT_DIR


DAY_NUM = 6
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
        total_yeses = 0

        for group in self.groups:
            answers = ''.join(group)
            group_yeses = len(set(answers))
            total_yeses += group_yeses

        return total_yeses

    @property
    def second(self):
        total_yeses = 0

        for group in self.groups:
            group_all_yeses = self.count_where_all_answered_yes(group)
            total_yeses += group_all_yeses

        return total_yeses

    def count_where_all_answered_yes(self, group):
        all_yeses = None

        for answers in group:
            answer_set = set(answers)
            if not all_yeses:
                all_yeses = answer_set
            else:
                all_yeses = all_yeses & answer_set

            if not all_yeses:
                return 0

        return len(all_yeses)

    #
    # Properties
    #
    @cached_property
    def groups(self):
        groups = []
        group = []

        for line in self.input_lines:
            if line == '':
                groups.append(group)
                group = []
            else:
                group.append(line)

        groups.append(group)
        return groups

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
