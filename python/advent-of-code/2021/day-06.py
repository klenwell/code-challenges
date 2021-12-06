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
        nums = self.input_lines[0].split(',')
        fishes = [int(n) for n in nums]
        days = 80

        for n in range(days):
            pop = []
            for fish in fishes:
                if fish > 0:
                    fish = fish-1
                else:
                    fish = 6
                    pop.append(8)

                pop.append(fish)

            fishes = pop.copy()
            print("Day {}".format(n), len(fishes))

        return len(fishes)

    @property
    def second(self):
        nums = self.input_lines[0].split(',')
        fishes = [LanternFish(int(n)) for n in nums]
        days = 80

        for n in range(days):
            for fish in fishes:
                fish.age()

            print("Day {}".format(n), sum([fish.offspring for fish in fishes]))

        return sum([fish.offspring for fish in fishes])

    @cached_property
    def input_lines(self):
        with open(self.input_file) as file:
            lines = file.readlines()
            return [line.strip() for line in lines]

    #
    # Methods
    #

class LanternFish:
    def __init__(self, due_days):
        self.due_days = due_days
        self.offspring = 1

    def age(self):
        self.due_days -= 1
        if self.due_days == -1:
            self.reproduce()

    def reproduce(self):
        self.offspring *= 2
        self.due_days = 7

    def __repr__(self):
        return "Fish(due={}, offspring={})".format(self.due_days, self.offspring)


#
# Main
#
solution = Solution(INPUT_FILE)
print("pt 1 solution: {}".format(solution.first))
print("pt 2 solution: {}".format(solution.second))
