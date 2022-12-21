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

    def __repr__(self):
        return '<Cube pt={}>'.format(self.pt)


class LavaDroplet:
    def __init__(self, scan_lines):
        self.scan_lines = scan_lines

    @cached_property
    def surface_area(self):
        area = 0
        pts = set()
        for cube in self.cubes:
            area += 6
            pts.add(cube.pt)
            for pt in cube.neighbors:
                if pt in pts:
                    area -= 2
        return area

    @cached_property
    def exterior_surface_area(self):
        area = 0
        pts = set()
        for cube in self.cubes:
            area += 6
            pts.add(cube.pt)
            for pt in cube.neighbors:
                if pt in pts:
                    area -= 2
                elif pt in self.air_cube_pts:
                    area -= 1
        return area

    @cached_property
    def min_x(self):
        return min([c.x for c in self.cubes])

    @cached_property
    def max_x(self):
        return max([c.x for c in self.cubes])

    @cached_property
    def min_y(self):
        return min([c.y for c in self.cubes])

    @cached_property
    def max_y(self):
        return max([c.y for c in self.cubes])

    @cached_property
    def min_z(self):
        return min([c.z for c in self.cubes])

    @cached_property
    def max_z(self):
        return max([c.z for c in self.cubes])

    @cached_property
    def cubes(self):
        cubes = []
        for line in self.scan_lines:
            x, y, z = [int(n) for n in line.split(',')]
            cube = Cube(x, y, z)
            cubes.append(cube)
        return cubes

    @cached_property
    def cube_pts(self):
        return [c.pt for c in self.cubes]

    @cached_property
    def air_cube_pts(self):
        cube_pts = []
        for x in range(self.min_x, self.max_x + 1):
            for y in range(self.min_y, self.max_y + 1):
                for z in range(self.min_z, self.max_z + 1):
                    pt = (x, y, z)
                    if pt not in self.cube_pts and self.is_interior_pt(pt):
                        cube_pts.append(pt)
        return cube_pts

    def is_interior_pt(self, pt):
        (x, y, z) = pt

        # In row (x)
        xs = self.yz_slices.get((y, z))
        if not xs or x < min(xs) or x > max(xs):
            return False

        # In col (y)
        ys = self.xz_slices.get((x, z))
        if not ys or y < min(ys) or y > max(ys):
            return False

        # In tube (z) - https://stats.stackexchange.com/a/588492
        zs = self.xy_slices.get((x, y))
        if not zs or z < min(zs) or z > max(zs):
            return False

        # It is trapped
        return True

    @cached_property
    def yz_slices(self):
        yz_slices = {}
        for x, y, z in self.cube_pts:
            yz = (y, z)
            if yz in yz_slices:
                yz_slices[yz].append(x)
            else:
                yz_slices[yz] = [x]
        return yz_slices

    @cached_property
    def xz_slices(self):
        xz_slices = {}
        for x, y, z in self.cube_pts:
            xz = (x, z)
            if xz in xz_slices:
                xz_slices[xz].append(y)
            else:
                xz_slices[xz] = [y]
        return xz_slices

    @cached_property
    def xy_slices(self):
        xy_slices = {}
        for x, y, z in self.cube_pts:
            xy = (x, y)
            if xy in xy_slices:
                xy_slices[xy].append(z)
            else:
                xy_slices[xy] = [z]
        return xy_slices


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
        droplet = LavaDroplet(self.input_lines)
        return droplet.surface_area

    @property
    def test2(self):
        droplet = LavaDroplet(self.test_input_lines)
        assert droplet.air_cube_pts == [(2, 2, 5)]
        return droplet.exterior_surface_area

    @property
    def second(self):
        droplet = LavaDroplet(self.input_lines)
        return droplet.exterior_surface_area
        # 972 (too low)
        # 2470 (too low)

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
