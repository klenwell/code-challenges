"""
Advent of Code 2021 - Day 09
https://adventofcode.com/2021/day/9
"""
from os.path import join as path_join
from functools import cached_property
from config import INPUT_DIR
from math import prod


INPUT_FILE = path_join(INPUT_DIR, 'day-09.txt')


class Solution:
    def __init__(self, input_file):
        self.input_file = input_file

    #
    # Solutions
    #
    @property
    def first(self):
        risk_level = 0
        for (x, y) in self.low_points:
            risk = self.grid[(x, y)]
            risk_level += risk + 1
        return risk_level

    @property
    def second(self):
        top_3_basins = sorted(self.basins, key=lambda b: b.size, reverse=True)[0:3]
        return prod([b.size for b in top_3_basins])

    #
    # Properties
    #
    @cached_property
    def input_lines(self):
        with open(self.input_file) as file:
            lines = file.readlines()
            return [line.strip() for line in lines]

    @cached_property
    def basins(self):
        basins = []
        for low_point in self.low_points:
            basin = Basin(low_point, self.grid)
            basins.append(basin)
        return basins

    @cached_property
    def low_points(self):
        low_points = []

        for x in range(self.row_count):
            for y in range(self.column_count):
                if self.is_low_point(x, y):
                    low_points.append((x, y))

        return low_points

    @cached_property
    def grid(self):
        grid_map = {}
        for x, line in enumerate(self.input_lines):
            cols = list(line)
            for y, val in enumerate(cols):
                grid_map[(x, y)] = int(val)
        return grid_map

    @cached_property
    def row_count(self):
        return len(self.input_lines)

    @cached_property
    def column_count(self):
        return len(self.input_lines[0])

    #
    # Methods
    #
    def is_low_point(self, x, y):
        default_value = 100

        pt = self.grid[(x, y)]
        n = self.grid.get((x, y-1), default_value)
        s = self.grid.get((x, y+1), default_value)
        e = self.grid.get((x+1, y), default_value)
        w = self.grid.get((x-1, y), default_value)

        for dir in (n, s, e, w):
            if pt >= dir:
                return False

        return True


class Basin:
    def __init__(self, low_point, grid):
        self.low_point = low_point
        self.grid = grid

    @property
    def size(self):
        return len(self.pts)

    @cached_property
    def pts(self):
        basin_pts = set()
        survey_pts = [self.low_point]
        surveyed_pts = []

        while len(survey_pts) > 0:
            survey_pt = survey_pts.pop(0)
            surveyed_pts.append(survey_pt)
            inner_pts = self.survey_basin(survey_pt)
            basin_pts = basin_pts.union(set(inner_pts))
            survey_pts += [ip for ip in inner_pts if ip not in surveyed_pts]

        return list(basin_pts)

    def survey_basin(self, pt):
        """Check adjacent points on the grid. Any that are less than 9 are
        considered inside the basin.
        """
        inner_pts = []
        default_value = 9
        (x, y) = pt

        n = (x, y-1)
        s = (x, y+1)
        e = (x+1, y)
        w = (x-1, y)

        for adj_pt in (n, s, e, w):
            height = self.grid.get(adj_pt, default_value)
            if height < 9:
                inner_pts.append(adj_pt)

        return inner_pts


#
# Main
#
solution = Solution(INPUT_FILE)
print("pt 1 solution: {}".format(solution.first))
print("pt 2 solution: {}".format(solution.second))
