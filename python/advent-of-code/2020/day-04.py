"""
Advent of Code 2020 - Day 04
https://adventofcode.com/2020/day/4
"""
from os.path import join as path_join
from functools import cached_property
from config import INPUT_DIR


INPUT_FILE = path_join(INPUT_DIR, 'day-04.txt')


class Solution:
    def __init__(self, input_file):
        self.input_file = input_file

    #
    # Properties
    #
    @property
    def first(self):
        valid_passports = 0
        
        for passport in self.passports:
            if self.is_valid(passport):
                valid_passports += 1

        return valid_passports


    @property
    def second(self):
        pass

    @cached_property
    def input_lines(self):
        with open(self.input_file) as file:
            lines = file.readlines()
            return [line.strip() for line in lines]

    @cached_property
    def batches(self):
        with open(self.input_file, 'r') as file:
            data = file.read()
            return data.split("\n\n")

    @cached_property
    def passports(self):
        passports = []

        for batch in self.batches:
            passport = {}
            fields = batch.split()
            for field in fields:
                k, v = field.split(':')
                passport[k] = v
            passports.append(passport)

        return passports

    #
    # Methods
    #
    def is_valid(self, passport):
        required_fields = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']
        fields = passport.keys()
        return len(set(required_fields) - set(fields)) == 0


#
# Main
#
solution = Solution(INPUT_FILE)
print("pt 1 solution: {}".format(solution.first))
print("pt 2 solution: {}".format(solution.second))
