"""
Advent of Code 2021 - Day 05
https://adventofcode.com/2021/day/5
"""
from os.path import join as path_join
from functools import cached_property
from config import INPUT_DIR


INPUT_FILE = path_join(INPUT_DIR, 'day-05.txt')


class Solution:
    def __init__(self, input_file):
        self.input_file = input_file
        self.grid = {}

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
        self.grid = {}

        for segment in self.segments:
            if self.is_diagonal(segment):
                continue

            pts = self.segment_to_pts(segment)
            for pt in pts:
                if pt in self.grid:
                    self.grid[pt] += 1
                else:
                    self.grid[pt] = 1

        return len([v for v in self.grid.values() if v > 1])

    @property
    def second(self):
        self.grid = {}

        for segment in self.segments:
            pts = self.segment_to_pts(segment)
            for pt in pts:
                if pt in self.grid:
                    self.grid[pt] += 1
                else:
                    self.grid[pt] = 1

        return len([v for v in self.grid.values() if v > 1])

    @cached_property
    def segments(self):
        segments = []

        for line in self.input_lines:
            segment = self.parse_line(line)
            segments.append(segment)

        return segments

    @cached_property
    def axis(self):
        return ((self.min_x, self.max_x), (self.min_y, self.max_y))

    @cached_property
    def min_x(self):
        xs = []
        for segment in self.segments:
            xs.append(segment[0][0])
            xs.append(segment[1][0])
        return min(xs)

    @cached_property
    def max_x(self):
        xs = []
        for segment in self.segments:
            xs.append(segment[0][0])
            xs.append(segment[1][0])
        return max(xs)

    @cached_property
    def min_y(self):
        ys = []
        for segment in self.segments:
            ys.append(segment[0][1])
            ys.append(segment[1][1])
        return min(ys)

    @cached_property
    def max_y(self):
        ys = []
        for segment in self.segments:
            ys.append(segment[0][1])
            ys.append(segment[1][1])
        return max(ys)

    #
    # Methods
    #
    def parse_line(self, line):
        csv1, csv2 = line.split('->')
        return (self.csv_to_pt(csv1), self.csv_to_pt(csv2))

    def csv_to_pt(self, csv):
        x, y = csv.split(',')
        return (int(x.strip()), int(y.strip()))

    def is_diagonal(self, segment):
        x = segment[0][0]
        y = segment[0][1]
        x1 = segment[1][0]
        y1 = segment[1][1]

        if x == x1:
            return False
        elif y == y1:
            return False
        else:
            return True

    def segment_to_pts(self, segment):
        if self.is_diagonal(segment):
            return self.diagonal_segment_to_pts(segment)
        else:
            return self.nondiagonal_segment_to_pts(segment)

    def diagonal_segment_to_pts(self, segment):
        pts = []
        x = segment[0][0]
        y = segment[0][1]
        x1 = segment[1][0]
        y1 = segment[1][1]

        dx = x1 - x
        dy = y1 - y
        nx = 1 if dx > 0 else -1
        ny = 1 if dy > 0 else -1

        for n in range(0, abs(dx)+1):
            xn = x + (nx * n)
            yn = y + (ny * n)
            pt = (xn, yn)
            pts.append(pt)

        return pts

    def nondiagonal_segment_to_pts(self, segment):
        pts = []
        x = segment[0][0]
        y = segment[0][1]
        x1 = segment[1][0]
        y1 = segment[1][1]

        if x != x1:
            n0 = min(x, x1)
            n1 = max(x, x1)
            for n in range(n0, n1+1):
                pts.append((n,y))
        elif y != y1:
            n0 = min(y, y1)
            n1 = max(y, y1)
            for n in range(n0, n1+1):
                pts.append((x,n))
        else:
            raise ValueError("Unexpected segment: {}".format(segment))

        return pts


#
# Main
#
solution = Solution(INPUT_FILE)
segment = solution.segments[4]
pts = solution.segment_to_pts(segment)
print(pts)
print(len(pts))
print(segment)
print("pt 1 solution: {}".format(solution.first))
print("pt 2 solution: {}".format(solution.second))
breakpoint()
