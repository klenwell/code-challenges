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
