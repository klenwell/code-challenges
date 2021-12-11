"""
Advent of Code 2021 - Day 11
https://adventofcode.com/2021/day/11
"""
from os.path import join as path_join
from functools import cached_property
from config import INPUT_DIR


INPUT_FILE = path_join(INPUT_DIR, 'day-11.txt')


class Solution:
    def __init__(self, input_file):
        self.input_file = input_file
        self.grid = {}

    #
    # Solutions
    #
    @property
    def first(self):
        total_flashes = 0
        self.reset_grid()

        for step in range(100):
            flashes = self.step()
            total_flashes += flashes
        return total_flashes

    @property
    def second(self):
        steps = 0
        self.reset_grid()

        while True:
            steps += 1
            flashes = self.step()
            self.print_grid()
            print(steps)
            if flashes == len(self.pts):
                return steps

    #
    # Properties
    #
    @cached_property
    def input_lines(self):
        with open(self.input_file) as file:
            lines = file.readlines()
            return [line.strip() for line in lines]

    @cached_property
    def pts(self):
        return self.grid.keys()

    #
    # Methods
    #
    def reset_grid(self):
        self.grid = {}

        for y, line in enumerate(self.input_lines):
            cols = list(line)
            for x, energy in enumerate(cols):
                self.grid[(x, y)] = int(energy)

        return self.grid

    def print_grid(self):
        for y in range(10):
            line = []
            for x in range(10):
                n = self.grid[(x, y)]
                chr = '*' if n == 0 else str(n)
                line.append(chr)
            print(''.join(line))

    def step(self):
        flashers = set()
        new_flashers = self.energize()

        while new_flashers:
            flashers = flashers.union(new_flashers)
            new_flashers = self.flash(new_flashers)
            new_flashers = new_flashers - flashers

        self.reset(flashers)
        return len(flashers)

    def energize(self):
        flashers = []
        for pt in self.pts:
            self.grid[pt] += 1
            if self.grid[pt] > 9:
                flashers.append(pt)
        return flashers

    def flash(self, flashers):
        new_flashers = set()

        for pt in flashers:
            new_flashers = new_flashers.union(self.energize_neighbors(pt))

        return new_flashers

    def reset(self, flashers):
        for pt in flashers:
            self.grid[pt] = 0

    def energize_neighbors(self, pt):
        flashers = set()
        x, y = pt

        n  = (x, y+1)
        ne = (x+1, y+1)
        e  = (x+1, y)
        se = (x+1, y-1)
        s  = (x, y-1)
        sw = (x-1, y-1)
        w  = (x-1, y)
        nw = (x-1, y+1)

        for pt in (n, ne, e, se, s, sw, w, nw):
            if not self.grid.get(pt):
                continue

            self.grid[pt] += 1
            if self.grid[pt] > 9:
                flashers.add(pt)

        return flashers




#
# Main
#
solution = Solution(INPUT_FILE)
print("pt 1 solution: {}".format(solution.first))
print("pt 2 solution: {}".format(solution.second))
