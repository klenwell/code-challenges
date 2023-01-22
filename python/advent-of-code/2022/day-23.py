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
            print(f"Round {n+1}")
            self.run_round()
            #self.print_map()
            #breakpoint()
        return len(self.empty_pts)

    def run_round(self):
        self.elves_propose_moves()
        self.elves_move()
        self.elves_rotate_proposed_directions()

    def elves_propose_moves(self):
        for elf in self.elves:
            elf.proposes_move(self)
        return self

    def elves_move(self):
        # Count proposed moves
        move_count = {}
        for elf in self.elves:
            move = elf.proposed_move
            if not move:
                continue
            if move in move_count:
                move_count[move] += 1
            else:
                move_count[move] = 1

        for elf in self.elves:
            if elf.proposed_move and move_count[elf.proposed_move] < 2:
                elf.moves()
        return self

    def elves_rotate_proposed_directions(self):
        for elf in self.elves:
            elf.rotate_proposed_directions()
        return self

    def pts_are_empty(self, pts):
        occupied_pts = self.elf_pts.intersection(set(pts))
        return len(occupied_pts) == 0

    def print_map(self):
        lines = []
        for y in range(self.min_y, self.max_y+1):
            tiles = []
            for x in range(self.min_x, self.max_x+1):
                tile = '.'
                for elf in self.elves:
                    if elf.pt == (x, y):
                        tile = '#'
                tiles.append(tile)
                line = ''.join(tiles)
            lines.append(line)
        map = '\n'.join(lines)
        print(map)
        return map


class Elf:
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y
        self.proposed_move = None
        self.proposed_directions = list('NSWE')

    @property
    def pt(self):
        return (self.x, self.y)

    @property
    def direction_delta(self):
        return {
            'N': (0, -1),
            'NE': (1, -1),
            'E': (1, 0),
            'SE': (1, 1),
            'S': (0, 1),
            'SW': (-1, 1),
            'W': (-1, 0),
            'NW': (-1, -1)
        }

    @property
    def adjacent_pts(self):
        pts = set()
        for dir in self.direction_delta.keys():
            pt = self.get_adjacent_pt(dir)
            pts.add(pt)
        return pts

    def proposes_move(self, grove):
        # During the first half of each round, each Elf considers the eight positions
        # adjacent to themself. If no other Elves are in one of those eight positions,
        # the Elf does not do anything during this round.
        if not self.elves_are_adjacent(grove):
            self.proposed_move = None
            return None

        # Otherwise, the Elf looks  in each of four directions in the following order
        # and proposes moving one step in the first valid direction:
        for proposed_dir in self.proposed_directions:
            if self.proposed_direction_is_valid(proposed_dir, grove):
                self.proposed_move = self.get_adjacent_pt(proposed_dir)
                return proposed_dir

        #breakpoint()
        self.proposed_move = None
        return None

    def elves_are_adjacent(self, grove):
        other_elf_pts = set([elf.pt for elf in grove.elves if elf != self])
        adjacent_elf_pts = self.adjacent_pts.intersection(other_elf_pts)
        #print(self.id, len(self.adjacent_pts), len(other_elf_pts), len(adjacent_elf_pts))
        #breakpoint()
        return len(adjacent_elf_pts) > 0

    def moves(self):
        if not self.proposed_move:
            return self.pt

        x, y = self.proposed_move
        self.x = x
        self.y = y
        self.proposed_move = None
        return self.pt

    def rotate_proposed_directions(self):
        dir = self.proposed_directions.pop(0)
        self.proposed_directions.append(dir)
        return (dir, self.proposed_directions[0])

    def proposed_direction_is_valid(self, dir, grove):
        # If no Elf in the N, NE, or NW adjacent positions, the Elf proposes moving north one step.
        # If no Elf in the S, SE, or SW adjacent positions, the Elf proposes moving south one step.
        # If no Elf in the W, NW, or SW adjacent positions, the Elf proposes moving west one step.
        # If no Elf in the E, NE, or SE adjacent positions, the Elf proposes moving east one step.
        mapped_points = {
            'N': ['N', 'NE', 'NW'],
            'S': ['S', 'SE', 'SW'],
            'W': ['W', 'NW', 'SW'],
            'E': ['E', 'NE', 'SE']
        }
        adjacent_dirs = mapped_points[dir]
        pts = self.get_adjacent_pts(adjacent_dirs)
        return grove.pts_are_empty(pts)

    def get_adjacent_pts(self, dirs):
        pts = []
        for dir in dirs:
            pt = self.get_adjacent_pt(dir)
            pts.append(pt)
        return pts

    def get_adjacent_pt(self, dir):
        dx, dy = self.direction_delta[dir]
        return (self.x + dx, self.y + dy)


class Solution:
    def __init__(self, input_file):
        self.input_file = input_file

    #
    # Solutions
    #
    @property
    def test1(self):
        # Arrange
        input = self.test_input_lines
        rounds = 10
        grove = Grove(input)

        # Assume
        assert len(grove.elves) == 22, len(grove.elves)
        assert len(grove.pts) == 49, len(grove.pts)
        assert len(grove.empty_pts) == 27, len(grove.empty_pts)

        # Act
        #grove.print_map()
        empty_pts = grove.plant_seedlings(rounds)

        # Assert
        assert empty_pts == 110, empty_pts
        return empty_pts

    @property
    def first(self):
        input = self.input_lines
        rounds = 10

        grove = Grove(input)
        empty_pts = grove.plant_seedlings(rounds)

        assert empty_pts == 3800, empty_pts
        return empty_pts

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
