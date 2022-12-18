"""
Advent of Code 2022 - Day 14
https://adventofcode.com/2022/day/14
"""
from os.path import join as path_join
from functools import cached_property
from config import INPUT_DIR


INPUT_FILE = path_join(INPUT_DIR, 'day-14.txt')

TEST_INPUT = """\
498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9"""

SAND_SOURCE = [500, 0]


class AbysmalCave:
    def __init__(self, input):
        self.input = input.strip()
        self.sand_source = SAND_SOURCE
        self.filled_pts = set().union(self.rock_pts)
        self.grains = []
        self.sand_reached_abyss = False

    @cached_property
    def input_lines(self):
        return self.input.split('\n')

    @cached_property
    def y_max(self):
        return max([y for x,y in self.rock_pts])

    @cached_property
    def rock_pts(self):
        return self.scan_rocks()

    def reached_abyss(self, grain):
        return grain[1] > self.y_max + 1

    def drop_grain(self):
        grain = (self.sand_source[0], self.sand_source[1])
        falling = True

        while falling:
            if self.reached_abyss(grain):
                self.sand_reached_abyss = True
                return grain

            # A unit of sand always falls down one step if possible.
            grain = (grain[0], grain[1]+1)

            # If the tile immediately below is blocked (by rock or sand)
            if grain in self.filled_pts:

                # the unit of sand attempts to instead move diagonally one step down and to the left
                grain = (grain[0]-1, grain[1])

                # If that tile is blocked
                if grain in self.filled_pts:

                    # the unit of sand attempts to instead move diagonally one step down and to the right
                    grain = (grain[0]+2, grain[1])

                    # If all three possible destinations are blocked, the unit of sand comes to rest and no longer moves
                    if grain in self.filled_pts:
                        grain = (grain[0]-1, grain[1]-1)
                        falling = False

        self.filled_pts.add(grain)
        self.grains.append(grain)
        return grain

    def scan_rocks(self):
        pts = set()
        for scan_line in self.input_lines:
            path_pts = []
            xy_pairs = scan_line.split(' -> ')
            for xy_pair in xy_pairs:
                x, y = xy_pair.strip().split(',')
                pt = (int(x), int(y))
                path_pts.append(pt)
                pts = pts.union(self.rock_path_to_pts(path_pts))
        return pts

    def rock_path_to_pts(self, rock_paths):
        pts = set()
        for n in range(len(rock_paths) - 1):
            x0, y0 = rock_paths[n]
            x1, y1 = rock_paths[n+1]

            # Vertical line
            if x0 == x1:
                for y in range(min(y0, y1), max(y0, y1) + 1):
                    pt = (x0, y)
                    pts.add(pt)
            # Horizontal line (assumes no diagnols)
            else:
                for x in range(min(x0, x1), max(x0, x1) + 1):
                    pt = (x, y0)
                    pts.add(pt)
        return pts


class FlooredCave(AbysmalCave):
    def __init__(self, input):
        super().__init__(input)
        self.blocked = False

    @cached_property
    def y_floor(self):
        return self.y_max + 2

    def tile_is_blocked(self, grain):
        if grain[1] >= self.y_floor:
            return True

        if grain in self.filled_pts:
            return True

        return False


    def drop_grain(self):
        grain = (self.sand_source[0], self.sand_source[1])
        falling = True

        while falling:
            if self.reached_abyss(grain):
                self.sand_reached_abyss = True
                return grain

            # A unit of sand always falls down one step if possible.
            grain = (grain[0], grain[1]+1)

            # If the tile immediately below is blocked (by rock or sand)
            if self.tile_is_blocked(grain):

                # the unit of sand attempts to instead move diagonally one step down and to the left
                grain = (grain[0]-1, grain[1])

                # If that tile is blocked
                if self.tile_is_blocked(grain):

                    # the unit of sand attempts to instead move diagonally one step down and to the right
                    grain = (grain[0]+2, grain[1])

                    # If all three possible destinations are blocked, the unit of sand comes to rest and no longer moves
                    if self.tile_is_blocked(grain):
                        grain = (grain[0]-1, grain[1]-1)
                        falling = False

        if grain[0] == self.sand_source[0] and grain[1] == self.sand_source[1]:
            self.blocked = True

        self.filled_pts.add(grain)
        self.grains.append(grain)
        return grain


class Solution:
    def __init__(self, input_file):
        self.input_file = input_file

    #
    # Solutions
    #
    @property
    def test1(self):
        cave = AbysmalCave(TEST_INPUT)
        print(cave.y_max, sorted(cave.filled_pts))

        while not cave.sand_reached_abyss:
            print(cave.drop_grain())

        return len(cave.grains)

    @property
    def first(self):
        cave = AbysmalCave(self.file_input)

        while not cave.sand_reached_abyss:
            cave.drop_grain()

        return len(cave.grains)

    @property
    def test2(self):
        cave = FlooredCave(TEST_INPUT)

        while not cave.blocked:
            print(cave.drop_grain())

        return len(cave.grains)

    @property
    def second(self):
        cave = FlooredCave(self.file_input)

        while not cave.blocked:
            cave.drop_grain()
            if len(cave.grains) % 100 == 0:
                print(len(cave.grains))

        return len(cave.grains)

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
