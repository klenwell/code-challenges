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

        print(sorted(grid.keys()))
        print(sorted(mirror_grid.keys()))
        print(first_fold)

        axis, pos = first_fold
        overlay_grid = self.fold_grid_over(mirror_grid, pos)
        merged_grid = self.overlay_grid(grid, overlay_grid)
        dots = len(merged_grid.keys())

        assert max([x for (x, y) in merged_grid.keys()]) <= pos
        print(sorted(merged_grid.keys()))

        # wrong: 464
        # 958
        return dots

    def overlay_grid(self, grid, overlay):
        new_grid = dict(grid)

        for pt, dot in overlay.items():
            new_grid[pt] = dot

        return new_grid


    def fold_grid_over(self, grid, width):
        folded_grid = {}
        print(sorted(grid.keys()))
        for (x, y) in grid:
            xf = width - x + width
            if xf >= 0:
                folded_grid[(xf, y)] = 'x'

        return folded_grid

    @property
    def second(self):
        pass

    @property
    def grid_width(self):
        return len(self.input_lines[0])

    @property
    def grid_height(self):
        return len(self.input_lines)

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


#
# Main
#
solution = Solution(INPUT_FILE)
print("pt 1 solution: {}".format(solution.first))
print("pt 2 solution: {}".format(solution.second))
