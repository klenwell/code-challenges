"""
Advent of Code 2020 - Day 02
https://adventofcode.com/2020/day/2
"""
from os.path import join as path_join
from functools import cached_property
from config import INPUT_DIR


INPUT_FILE = path_join(INPUT_DIR, 'day-02.txt')


class Solution:
    def __init__(self, input_file):
        self.input_file = input_file

    #
    # Properties
    #
    @cached_property
    def input_lines(self):
        with open(self.input_file) as file:
            lines = file.readlines()
            return [line.strip() for line in lines]

    @property
    def first(self):
        valid_passwords = 0

        for line in self.input_lines:
            policy, password = self.parse_line(line)
            if self.is_valid_password(password, policy):
                valid_passwords += 1

        return valid_passwords

    @property
    def second(self):
        valid_passwords = 0

        for line in self.input_lines:
            policy, password = self.parse_line(line)
            if self.is_valid_v2_password(password, policy):
                valid_passwords += 1

        return valid_passwords

    #
    # Methods
    #
    def parse_line(self, line):
        policy, password = line.split(':')
        return policy.strip(), password.strip()

    def parse_policy(self, policy):
        min_max, char = policy.split(' ')
        min_, max_ = min_max.split('-')
        return int(min_), int(max_), char

    def is_valid_password(self, password, policy):
        min_, max_, char = self.parse_policy(policy)
        return password.count(char) in range(min_, max_+1)

    def is_valid_v2_password(self, password, policy):
        p1, p2, char = self.parse_policy(policy)
        is_match = lambda n: password[n-1] == char
        matches = list(filter(is_match, [p1, p2]))
        return len(matches) == 1


#
# Main
#
solution = Solution(INPUT_FILE)
print("pt 1 solution: {}".format(solution.first))
print("pt 2 solution: {}".format(solution.second))
