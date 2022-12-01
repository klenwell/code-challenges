"""
Advent of Code 2022 - Day 1
https://adventofcode.com/2022/day/1
"""
from os.path import join as path_join
from functools import cached_property
from config import INPUT_DIR


INPUT_FILE = path_join(INPUT_DIR, 'day-01.txt')


class Solution:
    def __init__(self, input_file):
        self.input_file = input_file

    #
    # Solutions
    #
    @property
    def first(self):
        return max(self.elf_calories(self.input_lines))


    @property
    def second(self):
        sorted_cals = sorted(self.elf_calories(self.input_lines), reverse=True)
        return sum(sorted_cals[:3])

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
    def elf_calories(self, inputs):
        calories = []

        elf_packs = '-'.join(inputs).split('--')
        for pack in elf_packs:
            cals = pack.split('-')
            total_cals = sum([int(c) for c in cals])
            calories.append(total_cals)

        return calories


#
# Main
#
solution = Solution(INPUT_FILE)
print("pt 1 solution: {}".format(solution.first))
print("pt 2 solution: {}".format(solution.second))
