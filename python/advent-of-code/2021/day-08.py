"""
Advent of Code 2021 - Day 08
https://adventofcode.com/2021/day/8
"""
from os.path import join as path_join
from functools import cached_property
from config import INPUT_DIR


INPUT_FILE = path_join(INPUT_DIR, 'day-08.txt')


class Solution:
    def __init__(self, input_file):
        self.input_file = input_file

    #
    # Properties
    #
    @property
    def first(self):
        unique_signal_digits = {
            # digit: signal input length
            1: 2,
            4: 4,
            7: 3,
            8: 7
        }
        unique_segment_digits = []
        input_signal_lengths = unique_signal_digits.values()

        for values in self.output_values:
            for value in values:
                if len(value) in input_signal_lengths:
                    unique_segment_digits.append(value)
        return len(unique_segment_digits)

    @property
    def second(self):
        pass

    @cached_property
    def input_lines(self):
        with open(self.input_file) as file:
            lines = file.readlines()
            return [line.strip() for line in lines]

    @cached_property
    def signal_patterns(self):
        patterns = []
        for line in self.input_lines:
            signals, _ = line.split('|')
            pattern = [p for p in signals.strip().split(' ')]
            patterns.append(pattern)
        return patterns

    @cached_property
    def output_values(self):
        values = []
        for line in self.input_lines:
            _, outputs = line.split('|')
            digits = [d for d in outputs.strip().split(' ')]
            values.append(digits)
        return values


    #
    # Methods
    #


#
# Main
#
solution = Solution(INPUT_FILE)
print("pt 1 solution: {}".format(solution.first))
print("pt 2 solution: {}".format(solution.second))
