"""
Advent of Code 2022 - Day 18
https://adventofcode.com/2022/day/18
"""
from os.path import join as path_join
from functools import cached_property
from config import INPUT_DIR


INPUT_FILE = path_join(INPUT_DIR, 'day-18.txt')

TEST_INPUT = """\
2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5"""


class Cube:
    def __init__(self, x, y, z):
        self.x = int(x)
        self.y = int(y)
        self.z = int(z)

    @property
    def pt(self):
        return (self.x, self.y, self.z)

    @cached_property
    def neighbors(self):
        return [
            (self.x-1, self.y, self.z),
            (self.x+1, self.y, self.z),
            (self.x, self.y-1, self.z),
            (self.x, self.y+1, self.z),
            (self.x, self.y, self.z-1),
            (self.x, self.y, self.z+1)
        ]


class Solution:
    def __init__(self, input_file):
        self.input_file = input_file

    #
    # Solutions
    #
    @property
    def test1(self):
        area = 0
        pts = set()
        for line in self.test_input_lines:
            area += 6
            x, y, z = [int(n) for n in line.split(',')]
            cube = Cube(x, y, z)
            pts.add(cube.pt)
            for pt in cube.neighbors:
                if pt in pts:
                    area -= 2
        return area

    @property
    def first(self):
        area = 0
        pts = set()
        for line in self.input_lines:
            area += 6
            x, y, z = [int(n) for n in line.split(',')]
            cube = Cube(x, y, z)
            pts.add(cube.pt)
            for pt in cube.neighbors:
                if pt in pts:
                    area -= 2
        return area

    @property
    def test2(self):
        surface_area = 0
        filled_pts = set()
        all_pts = set()
        for line in self.test_input_lines:
            surface_area += 6
            x, y, z = [int(n) for n in line.split(',')]
            cube = Cube(x, y, z)
            filled_pts.add(cube.pt)
            for pt in cube.neighbors:
                all_pts.add(pt)
                if pt in filled_pts:
                    surface_area -= 2

        empty_pts = all_pts - filled_pts

        min_x = min([p[0] for p in filled_pts])
        max_x = max([p[0] for p in filled_pts])
        min_y = min([p[1] for p in filled_pts])
        max_y = max([p[1] for p in filled_pts])
        min_z = min([p[2] for p in filled_pts])
        max_z = max([p[2] for p in filled_pts])

        inner_empty_pts = set()
        for x, y, z in empty_pts:
            inner_x = x > min_x and x < max_x
            inner_y = y > min_y and y < max_y
            inner_z = z > min_z and z < max_z
            if inner_x and inner_y and inner_z:
                inner_empty_pts.add((x, y, z))

        print(inner_empty_pts)

        return surface_area - (len(inner_empty_pts) * 6)

    @property
    def second(self):
        surface_area = 0
        filled_pts = set()
        all_pts = set()
        for line in self.input_lines:
            surface_area += 6
            x, y, z = [int(n) for n in line.split(',')]
            cube = Cube(x, y, z)
            filled_pts.add(cube.pt)
            for pt in cube.neighbors:
                all_pts.add(pt)
                if pt in filled_pts:
                    surface_area -= 2

        empty_pts = all_pts - filled_pts

        min_x = min([p[0] for p in filled_pts])
        max_x = max([p[0] for p in filled_pts])
        min_y = min([p[1] for p in filled_pts])
        max_y = max([p[1] for p in filled_pts])
        min_z = min([p[2] for p in filled_pts])
        max_z = max([p[2] for p in filled_pts])

        inner_empty_pts = set()
        for x, y, z in empty_pts:
            inner_x = x > min_x and x < max_x
            inner_y = y > min_y and y < max_y
            inner_z = z > min_z and z < max_z
            if inner_x and inner_y and inner_z:
                inner_empty_pts.add((x, y, z))

        print(len(filled_pts), len(inner_empty_pts), surface_area)

        # Subtract inner area pts
        for x, y, z in filled_pts:
            cube = Cube(x, y, z)
            for pt in cube.neighbors:
                if pt in inner_empty_pts:
                    print(cube.pt, pt)
                    surface_area -= 2

        return surface_area
        # 972 (too low)

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
    # Methods
    #


#
# Main
#
solution = Solution(INPUT_FILE)
print("test 1 solution: {}".format(solution.test1))
print("pt 1 solution: {}".format(solution.first))
print("test 2 solution: {}".format(solution.test2))
print("pt 2 solution: {}".format(solution.second))
