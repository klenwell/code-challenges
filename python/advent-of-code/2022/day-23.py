"""
Advent of Code 2022 - Day 23
https://adventofcode.com/2022/day/23

Unstable Diffusion
"""
from os.path import join as path_join
from functools import cached_property
from config import INPUT_DIR


INPUT_FILE = path_join(INPUT_DIR, 'day-23.txt')

TEST_INPUT = """\
....#..
..###.#
#...#.#
.#...##
#.###..
##.#.##
.#..#.."""


class Grove:
    def __init__(self, scan_lines):
        self.scan_lines = scan_lines
        self.tiles = self.add_tiles(scan_lines)
        self.elves = self.add_elves(self.tiles)

    def add_tiles(self, scan_lines):
        tiles = {}
        for y, line in enumerate(scan_lines):
            for x, tile in enumerate(line):
                pt = (x, y)
                tiles[pt] = tile
        return tiles

    def add_elves(self, tiles):
        elves = []
        n = 0

        for pt, tile in tiles.items():
            if tile == '#':
                n += 1
                x, y = pt
                elf = Elf(n, x, y)
                elves.append(elf)

        return elves

    @property
    def min_x(self):
        return min(elf.x for elf in self.elves)

    @property
    def max_x(self):
        return max(elf.x for elf in self.elves)

    @property
    def min_y(self):
        return min(elf.y for elf in self.elves)

    @property
    def max_y(self):
        return max(elf.y for elf in self.elves)

    @property
    def pts(self):
        pts = set()
        for x in range(self.min_x, self.max_x+1):
            for y in range(self.min_y, self.max_y+1):
                pt = (x, y)
                pts.add(pt)
        return pts

    @property
    def elf_pts(self):
        pts = set()
        for elf in self.elves:
            pts.add(elf.pt)
        return pts

    @property
    def empty_pts(self):
        return self.pts - self.elf_pts

    def plant_seedlings(self, num_rounds):
        for n in range(num_rounds):
            self.run_round()
        return len(self.empty_pts)

    def run_round(self):
        self.elves_propose_moves()
        self.elves_move()

    def elves_propose_moves(self):
        todo

    def elves_move(self):
        todo


class Elf:
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y

    @property
    def pt(self):
        return (self.x, self.y)


class Solution:
    def __init__(self, input_file):
        self.input_file = input_file

    #
    # Solutions
    #
    @property
    def test1(self):
        input = self.test_input_lines

        grove = Grove(input)

        # Assumptions
        assert len(grove.elves) == 22, len(grove.elves)
        assert len(grove.pts) == 49, len(grove.pts)
        assert len(grove.empty_pts) == 27, len(grove.empty_pts)

        return grove

    @property
    def first(self):
        input = self.input_lines
        return input

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
# Main
#
solution = Solution(INPUT_FILE)
print(f"test 1 solution: {solution.test1}")
print(f"pt 1 solution: {solution.first}")
print(f"test 2 solution: {solution.test2}")
print(f"pt 2 solution: {solution.second}")
