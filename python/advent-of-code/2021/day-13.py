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

        return dots

    @property
    def second(self):
        dots = self.dots.copy()

        for axis, pos in self.folds:
            dots = self.fold(axis, pos, dots)
            print(len(dots))

        print(dots)
        self.print_dots(dots)
        return '^^^ See print out above ^^^'

    def print_dots(self, dots):
        max_y = max([y for (x, y) in dots])
        max_x = max([x for (x, y) in dots])

        for y in range(max_y + 1):
            row = []
            for x in range(max_x + 1):
                chr = '#' if (x, y) in dots else '.'
                row.append(chr)
            print(''.join(row))

    def fold(self, axis, pos, dots):
        if axis == 'x':
            return self.fold_left(pos, dots)
        else:
            return self.fold_up(pos, dots)

    def fold_left(self, fold_x, dots):
        left_dots = set()
        right_dots = set()

        for (x, y) in dots:
            if x < fold_x:
                left_dots.add((x, y))
            elif x > fold_x:
                xm = fold_x - x + fold_x
                right_dots.add((xm, y))

        return left_dots.union(right_dots)

    def fold_up(self, fold_y, dots):
        upper_dots = set()
        lower_dots = set()

        for (x, y) in dots:
            if y < fold_y:
                upper_dots.add((x, y))
            elif y > fold_y:
                ym = fold_y - y + fold_y
                lower_dots.add((x, ym))

        return upper_dots.union(lower_dots)


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
    def max_x(self):
        return max([x for (x, y) in self.dots])

    @property
    def max_y(self):
        return max([y for (x, y) in self.dots])

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

    @cached_property
    def grid(self):
        grid = {}
        dot_char = '#'
        blank_char = '.'

        for y in range(self.max_y + 1):
            print('grid', y)
            for x in range(self.max_x + 1):
                pt = (x, y)
                if pt in self.dots:
                    grid[pt] = dot_char
                else:
                    grid[pt] = blank_char

        return grid

    def print_grid(self, grid):
        max_x = max([x for (x, y) in grid.keys()])
        max_y = max([y for (x, y) in grid.keys()])

        for y in range(max_y + 1):
            row = []
            for x in range(max_x + 1):
                char = grid.get((x, y), '.')
                row.append(char)
            print(''.join(row))




    #
    # Methods
    #


#
# Main
#
solution = Solution(INPUT_FILE)
print("pt 1 solution: {}".format(solution.first))
print("pt 2 solution: {}".format(solution.second))
