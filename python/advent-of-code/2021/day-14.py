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
        steps = 10
        polymer = POLYMER_TEMPLATE

        for step in range(steps):
            polymer = solution.apply_insert_rules(polymer)

        element_counts = sorted(solution.count_elements(polymer))
        lce = element_counts[0]
        mce = element_counts[-1]

        return mce[0] - lce[0]

    @staticmethod
    def second():
        """Another counting exercise like Day 6.
        Source: https://old.reddit.com/r/adventofcode/comments/rg0ssd
        """
        solution = Solution(INPUT_FILE)
        steps = 40
        polymer = POLYMER_TEMPLATE
        element_counter = {}
        polymer_pairs = {}

        for el in polymer:
            element_counter[el] = element_counter.get(el, 0) + 1

        for n in range(len(polymer)-1):
            pair = polymer[n:n+2]
            polymer_pairs[pair] = polymer_pairs.get(pair, 0) + 1

        for step in range(steps):
            new_pairs = {}

            for old_pair, pair_count in polymer_pairs.items():
                insert = solution.insertion_rules[old_pair]
                left_pair = old_pair[0] + insert
                right_pair = insert + old_pair[1]

                # Update element and new pair counts
                element_counter[insert] += pair_count
                new_pairs[left_pair] = new_pairs.get(left_pair, 0) + pair_count
                new_pairs[right_pair] = new_pairs.get(right_pair, 0) + pair_count

            polymer_pairs = new_pairs

        return max(element_counter.values()) - min(element_counter.values())

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

    def count_elements(self, polymer):
        counter = {}
        for el in polymer:
            counter[el] = counter.get(el, 0) + 1
        return [(n, el) for el, n in counter.items()]

    def apply_insert_rules(self, polymer):
        chain = [polymer[0]]

        for n, elem in enumerate(list(polymer)):
            if n >= len(polymer) - 1:
                break

            next = polymer[n+1]
            insert = self.insertion_rules[elem + next]
            chain += [insert, next]

        return ''.join(chain)


#
# Main
#
print("pt 1 solution: {}".format(Solution.first()))
print("pt 2 solution: {}".format(Solution.second()))
