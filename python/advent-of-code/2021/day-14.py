"""
Advent of Code 2021 - Day 14
https://adventofcode.com/2021/day/14
"""
from os.path import join as path_join
from functools import cached_property
from config import INPUT_DIR


INPUT_FILE = path_join(INPUT_DIR, 'day-14.txt')
POLYMER_TEMPLATE = 'CNBPHFBOPCSPKOFNHVKV'


class Solution:
    #
    # Solutions
    #
    @staticmethod
    def first():
        solution = Solution(INPUT_FILE)
        print(solution.insertion_rules)

        steps = 10
        polymer = POLYMER_TEMPLATE

        for step in range(steps):
            polymer = solution.apply_insert_rules(polymer)
            print(polymer)

        element_counts = sorted(solution.count_elements(polymer))
        print(element_counts)
        lce = element_counts[0]
        mce = element_counts[-1]
        print(lce, mce)

        return mce[0] - lce[0]

    def count_elements(self, polymer):
        counter = {}
        for el in polymer:
            counter[el] = counter.get(el, 0) + 1
        return [(n, el) for el, n in counter.items()]

    def apply_insert_rules(self, polymer):
        #print(polymer)
        chain = []

        for n, elem in enumerate(list(polymer)):
            if n >= len(polymer) - 1:
                break

            next = polymer[n+1]
            insert = self.insertion_rules[elem + next]
            chain += [elem, insert, next]

        #print(chain)
        return ''.join(chain)

    @staticmethod
    def second():
        solution = Solution(INPUT_FILE)

    #
    # Properties
    #
    @cached_property
    def input_lines(self):
        with open(self.input_file) as file:
            lines = file.readlines()
            return [line.strip() for line in lines]

    @cached_property
    def insertion_rules(self):
        rules = {}
        for line in self.input_lines:
            pair, insert = line.split(' -> ')
            rules[pair] = insert
        return rules

    #
    # Methods
    #
    def __init__(self, input_file):
        self.input_file = input_file

#
# Main
#
print("pt 1 solution: {}".format(Solution.first()))
print("pt 2 solution: {}".format(Solution.second()))
