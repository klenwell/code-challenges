"""
Advent of Code 2022 - Day 22
https://adventofcode.com/2022/day/22
"""
from os.path import join as path_join
from functools import cached_property
from config import INPUT_DIR


INPUT_FILE = path_join(INPUT_DIR, 'day-22.txt')

TEST_INPUT = """\
"""


class PasswordDecoder:
    def __init__(self, input):
        pass

    @cached_property
    def board_map(self):
        pass

    @cached_property
    def path_code(self):
        pass

    @property
    def password(self):
        return self.decode_password()

    def decode_password(self):
        pass


class Solution:
    def __init__(self, input_file):
        self.input_file = input_file

    #
    # Solutions
    #
    @property
    def test1(self):
        input = TEST_INPUT
        decoder = PasswordDecoder(input)
        assert decoder.password == 6032, decoder.password
        return decoder.password

    @property
    def first(self):
        input = self.input_lines
        return input

    @property
    def test2(self):
        pass

    @property
    def second(self):
        pass

    #
    # Properties
    #
    @cached_property
    def file_input(self):
        with open(self.input_file) as file:
            return file.read().strip()

    @cached_property
    def input_lines(self):
        return [line.strip() for line in self.file_input.split("\n")]

    @cached_property
    def test_input_lines(self):
        return [line.strip() for line in TEST_INPUT.split("\n")]


#
# Main
#
solution = Solution(INPUT_FILE)
print(f"test 1 solution: {solution.test1}")
print(f"pt 1 solution: {solution.first}")
print(f"test 2 solution: {solution.test2}")
print(f"pt 2 solution: {solution.second}")
