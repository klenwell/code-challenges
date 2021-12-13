"""
Advent of Code 2021 - Day 13
https://adventofcode.com/2021/day/13
"""
from os.path import join as path_join
from functools import cached_property
from config import INPUT_DIR


INPUT_FILE = path_join(INPUT_DIR, 'day-13.txt')


class Solution:
    def __init__(self, input_file):
        self.input_file = input_file

    #
    # Solutions
    #
    @property
    def first(self):
        grid = {}
        mirror_grid = {}
        first_fold = self.folds[0]

        for pt in self.dots:
            if pt[0] < first_fold[1]:
                grid[pt] = 'x'
            elif pt[0] > first_fold[1]:
                mirror_grid[pt] = 'x'

        axis, pos = first_fold
        overlay_grid = self.fold_grid_over(mirror_grid, pos)
        merged_grid = self.overlay_grid(grid, overlay_grid)
        dots = len(merged_grid.keys())

        assert max([x for (x, y) in merged_grid.keys()]) <= pos
        return dots

    @property
    def second(self):
        dots = self.dots.copy()

        for axis, pos in self.folds:
            dots = self.fold(axis, pos, dots)

        self.print_dots(dots)
        return '^^^ See print out above ^^^'

    #
    # Properties
    #
    @cached_property
    def input_lines(self):
        with open(self.input_file) as file:
            lines = file.readlines()
            return [line.strip() for line in lines]

    @cached_property
    def dots(self):
        dots = []

        for line in self.input_lines:
            if not line:
                break

            x, y = line.split(',')
            dots.append((int(x), int(y)))

        return dots

    @cached_property
    def folds(self):
        folds = []
        start_parsing = False

        for line in self.input_lines:
            if not start_parsing:
                if not line:
                    start_parsing = True
                continue

            _, _, inst = line.split(' ')
            axis, val = inst.split('=')
            folds.append((axis, int(val)))

        return folds

    #
    # Methods
    #

    def fold(self, axis, pos, dots):
        if axis == 'x':
            return self.fold_left(pos, dots)
        else:
            return self.fold_up(pos, dots)

    def fold_left(self, x_fold, dots):
        left_dots = set()
        right_dots = set()

        for (x, y) in dots:
            if x < x_fold:
                left_dots.add((x, y))
            elif x > x_fold:
                xm = (2 * x_fold) - x
                right_dots.add((xm, y))

        return left_dots.union(right_dots)

    def fold_up(self, y_fold, dots):
        upper_dots = set()
        lower_dots = set()

        for (x, y) in dots:
            if y < y_fold:
                upper_dots.add((x, y))
            elif y > y_fold:
                ym = (2 * y_fold) - y
                lower_dots.add((x, ym))

        return upper_dots.union(lower_dots)

    def print_dots(self, dots):
        max_y = max([y for (x, y) in dots])
        max_x = max([x for (x, y) in dots])

        for y in range(max_y + 1):
            row = []
            for x in range(max_x + 1):
                chr = '#' if (x, y) in dots else ' '
                row.append(chr)
            print(''.join(row))

    def fold_grid_over(self, grid, width):
        folded_grid = {}
        for (x, y) in grid:
            xf = width - x + width
            if xf >= 0:
                folded_grid[(xf, y)] = 'x'
        return folded_grid

    def overlay_grid(self, grid, overlay):
        new_grid = dict(grid)
        for pt, dot in overlay.items():
            new_grid[pt] = dot
        return new_grid


#
# Main
#
solution = Solution(INPUT_FILE)
print("pt 1 solution: {}".format(solution.first))
print("pt 2 solution: {}".format(solution.second))
