"""
Advent of Code 2021 - Day 07
https://adventofcode.com/2021/day/7
"""
from os.path import join as path_join
from functools import cached_property
from config import INPUT_DIR


INPUT_FILE = path_join(INPUT_DIR, 'day-07.txt')


class Solution:
    def __init__(self, input_file):
        self.input_file = input_file

    #
    # Properties
    #
    @property
    def first(self):
        costs = []
        for n in range(max(self.crabs) + 1):
            fuel_cost = self.align_crabs(n)
            cost_pos = (fuel_cost, n)
            costs.append(cost_pos)
        return sorted(costs)[0][0]

    @property
    def second(self):
        # print("This will take a few seconds...")
        costs = []

        for n in range(max(self.crabs) + 1):
            fuel_cost = self.align_crabs_v2(n)
            cost_pos = (fuel_cost, n)
            costs.append(cost_pos)
            # self.print_countdown(n)

        return sorted(costs)[0][0]

    @cached_property
    def input_lines(self):
        with open(self.input_file) as file:
            lines = file.readlines()
            return [line.strip() for line in lines]

    @cached_property
    def crabs(self):
        return [int(n) for n in self.input_lines[0].split(',')]

    #
    # Methods
    #
    def align_crabs(self, pos):
        costs = []

        for crab_pos in self.crabs:
            cost = abs(crab_pos - pos)
            costs.append(cost)

        return sum(costs)

    def align_crabs_v2(self, pos):
        costs = []

        for crab_pos in self.crabs:
            steps = abs(crab_pos - pos)
            # cost = sum([n for n in range(1, steps+1)])
            # Much faster: https://stackoverflow.com/a/60348809/1093087
            cost = steps * (steps + 1) // 2
            costs.append(cost)

        return sum(costs)

    def print_countdown(self, n):
        seq1 = [0, 100, 200, 300, 500, 800, 1300]
        seq2 = [max(self.crabs)-n for n in range(1, 11)]

        if n in sorted(seq1 + seq2, reverse=True):
            print("{} loops to go".format(max(self.crabs) - n))


#
# Main
#
solution = Solution(INPUT_FILE)
print("pt 1 solution: {}".format(solution.first))
print("pt 2 solution: {}".format(solution.second))
