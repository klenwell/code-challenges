"""
Advent of Code 2022 - Day 5
https://adventofcode.com/2022/day/5

References:

"""
from os.path import join as path_join
from functools import cached_property
from config import INPUT_DIR


INPUT_FILE = path_join(INPUT_DIR, 'day-05.txt')


STACKS_DRAWING = """
[T]             [P]     [J]
[F]     [S]     [T]     [R]     [B]
[V]     [M] [H] [S]     [F]     [R]
[Z]     [P] [Q] [B]     [S] [W] [P]
[C]     [Q] [R] [D] [Z] [N] [H] [Q]
[W] [B] [T] [F] [L] [T] [M] [F] [T]
[S] [R] [Z] [V] [G] [R] [Q] [N] [Z]
[Q] [Q] [B] [D] [J] [W] [H] [R] [J]
"""


class Solution:
    def __init__(self, input_file):
        self.input_file = input_file

    #
    # Solutions
    #
    @property
    def first(self):
        stacks = self.parse_stacks(STACKS_DRAWING)
        for line in self.input_lines:
            num, from_col, to_col = self.parse_crate_movement(line)
            stacks = self.move_crates(stacks, num, from_col, to_col)
        stack_tops = [stacks[n+1][0] for n in range(9)]
        return ''.join(stack_tops)

    @property
    def second(self):
        stacks = self.parse_stacks(STACKS_DRAWING)
        for line in self.input_lines:
            num, from_col, to_col = self.parse_crate_movement(line)
            stacks = self.move_crates_with_9001(stacks, num, from_col, to_col)
        stack_tops = [stacks[n+1][0] for n in range(9)]
        return ''.join(stack_tops)

    #
    # Properties
    #
    @cached_property
    def input_lines(self):
        with open(self.input_file) as file:
            lines = file.readlines()
            return [line.strip() for line in lines]

    #
    # Methods
    #
    def move_crates_with_9001(self, stacks, num, from_col, to_col):
        crates = stacks[from_col][0:num]
        stacks[from_col] = stacks[from_col][num:]
        stacks[to_col] = crates + stacks[to_col]
        return stacks

    def move_crates(self, stacks, num, from_col, to_col):
        for n in range(num):
            crate = stacks[from_col].pop(0)
            stacks[to_col].insert(0, crate)
        return stacks

    def parse_crate_movement(self, line):
        # https://stackoverflow.com/a/4289557/1093087
        num, from_col, to_col = [int(s) for s in line.split() if s.isdigit()]
        return num, from_col, to_col

    def parse_stacks(self, drawing):
        stacks = dict([(n+1, []) for n in range(9)])
        lines = drawing.split("\n")

        for line in lines:
            if len(line) < 1:
                continue

            crates = self.parse_crates_in_row(line)

            for n in range(9):
                col = n+1
                crate = crates[n].strip()
                if crate:
                    stacks[col].append(crate)

        return stacks

    def parse_crates_in_row(self, line):
        columns = []
        step = 4
        for n in range(1, 35, step):
            try:
                crate = line[n]
            except IndexError:
                crate = ' '
            columns.append(crate)
        return columns


#
# Main
#
solution = Solution(INPUT_FILE)
print("pt 1 solution: {}".format(solution.first))
print("pt 2 solution: {}".format(solution.second))
