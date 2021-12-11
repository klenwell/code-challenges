"""
Advent of Code 2020 - Day 05
https://adventofcode.com/2020/day/5
"""
from os.path import join as path_join
from functools import cached_property
from config import INPUT_DIR


INPUT_FILE = path_join(INPUT_DIR, 'day-05.txt')


class Solution:
    def __init__(self, input_file):
        self.input_file = input_file

    #
    # Properties
    #
    @property
    def first(self):
        return max(self.seat_ids)

    @property
    def second(self):
        for left_seat in sorted(self.seat_ids):
            middle_seat = left_seat + 1
            right_seat = left_seat + 2
            print(left_seat, middle_seat, right_seat)
            if (middle_seat not in self.seat_ids) and (right_seat in self.seat_ids):
                return middle_seat

    @cached_property
    def input_lines(self):
        with open(self.input_file) as file:
            lines = file.readlines()
            return [line.strip() for line in lines]

    @property
    def seat_ids(self):
        seat_ids = []
        for seat_code in self.input_lines:
            seat_id = self.seat_code_to_id(seat_code)
            seat_ids.append(seat_id)
        return seat_ids

    #
    # Methods
    #
    def seat_code_to_id(self, code):
        # Compute row
        row_code = code[:7]
        row_bin = ''.join(['1' if c == 'B' else '0' for c in row_code])
        row = int(row_bin, 2)

        # Compute column
        col_code = code[7:]
        col_bin = ''.join(['1' if c == 'R' else '0' for c in col_code])
        col = int(col_bin, 2)

        # Compute id
        return row * 8 + col


#
# Main
#
solution = Solution(INPUT_FILE)
print("pt 1 solution: {}".format(solution.first))
print("pt 2 solution: {}".format(solution.second))
