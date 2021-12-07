"""
Advent of Code 2021 - Day 06
https://adventofcode.com/2021/day/6
"""
from os.path import join as path_join
from functools import cached_property
from config import INPUT_DIR


INPUT_FILE = path_join(INPUT_DIR, 'day-06.txt')


class Solution:
    def __init__(self, input_file):
        self.input_file = input_file

    #
    # Properties
    #
    @property
    def first(self):
        fishes = [int(n) for n in self.input_lines[0].split(',')]
        days = 80

        for n in range(days):
            next_gen = []
            for fish in fishes:
                if fish > 0:
                    fish = fish-1
                else:
                    fish = 6
                    next_gen.append(8)

                next_gen.append(fish)
            fishes = next_gen.copy()

        return len(fishes)

    @property
    def second(self):
        """As expected, the brutal approach in part 1 did not work. Could numpy arrays
        power through it? This Reddit comment tipped me off to solution here:
        https://old.reddit.com/r/adventofcode/comments/r9z49j/2021_day_6_solutions/hnffzni/
        """
        days = 256
        fishes = [int(n) for n in self.input_lines[0].split(',')]

        cohorts = [0] * 9
        for n in range(len(cohorts)):
            cohorts[n] = fishes.count(n)

        for n in range(days):
            cohorts = self.cycle_cohorts(cohorts)

        return sum(cohorts)

    @cached_property
    def input_lines(self):
        with open(self.input_file) as file:
            lines = file.readlines()
            return [line.strip() for line in lines]

    #
    # Methods
    #
    def cycle_cohorts(self, cohorts):
        newborns = cohorts.pop(0)
        cohorts.append(newborns)
        cohorts[6] += newborns
        return cohorts


#
# Main
#
solution = Solution(INPUT_FILE)
print("pt 1 solution: {}".format(solution.first))
print("pt 2 solution: {}".format(solution.second))
