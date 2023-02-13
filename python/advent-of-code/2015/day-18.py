"""
Advent of Code 2015 - Day 18
https://adventofcode.com/2015/day/18

Day 18: Like a GIF For Your Yard
"""
from os.path import join as path_join
from functools import cached_property
from common import INPUT_DIR, info


class Grid:
    def __init__(self, input):
        self.input = input.strip()
        self.grid = self.init_grid()

    @cached_property
    def rows(self):
        rows = []
        for line in self.input.split('\n'):
            row = list(line)
            rows.append(row)
        return rows

    @cached_property
    def pts(self):
        return list(self.grid.keys())

    @cached_property
    def min_x(self):
        return 0

    @cached_property
    def max_x(self):
        return len(self.rows[0]) - 1

    @cached_property
    def min_y(self):
        return 0

    @cached_property
    def max_y(self):
        return len(self.rows) - 1

    def init_grid(self):
        grid = {}
        for y, row in enumerate(self.rows):
            for x, val in enumerate(row):
                pt = (x, y)
                grid[pt] = val
        return grid

    def neighbors(self, pt):
        pts = []
        deltas = [  # Clockwise from NW to W
            (-1, -1), (0, -1), (1, -1), (1, 0),
            (1, 1), (0, 1), (-1, 1), (-1, 0)
        ]
        x, y = pt

        for dx, dy in deltas:
            nx = x + dx
            ny = y + dy

            if (self.min_x <= nx <= self.max_x) and (self.min_y <= ny <= self.max_y):
                npt = (nx, ny)
                pts.append(npt)

        return pts

    def cardinal_neighbors(self, pt):
        # N, S, E, W
        pts = []
        deltas = [(-1, 0), (1, 0), (1, 0), (-1, 0)]
        x, y = pt

        for dx, dy in deltas:
            nx = x + dx
            ny = y + dy

            if (self.min_x <= nx <= self.max_x) and (self.min_y <= ny <= self.max_y):
                npt = (nx, ny)
                pts.append(npt)

        return pts



class AnimatedLightGrid(Grid):
    @property
    def lit_lights(self):
        return [pt for pt in self.pts if self.grid[pt] == '#']

    def animate(self, steps):
        for n in range(steps):
            info(f"step {n}", 10)
            self.animate_step()
        return len(self.lit_lights)

    def animate_step(self):
        next_grid = {}
        for pt in self.pts:
            value = self.animate_pt(pt)
            next_grid[pt] = value
        self.grid = next_grid

    def animate_pt(self, pt):
        before = self.grid[pt]
        is_on = before == '#'
        neighbors_on = 0

        for npt in self.neighbors(pt):
            if self.grid[npt] == '#':
                neighbors_on += 1

        # A light which is on stays on when 2 or 3 neighbors are on, and turns off otherwise.
        if is_on:
            stays_on = neighbors_on in (2,3)
            after = '#' if stays_on else '.'

        # A light which is off turns on if exactly 3 neighbors are on, and stays off otherwise.
        else:
            turns_on = neighbors_on == 3
            after = '#' if turns_on else '.'

        return after


class AdventPuzzle:
    INPUT_FILE = path_join(INPUT_DIR, 'day-18.txt')

    TEST_INPUT = """\
.#.#.#
...##.
#....#
..#...
#.#..#
####.."""

    def solve(self):
        print(f"test 1 solution: {self.test1}")
        print(f"Part 1 Solution: {self.first}")
        print(f"test 2 solution: {self.test2}")
        print(f"Part 2 Solution: {self.second}")

    #
    # Solutions
    #
    @property
    def first(self):
        input = self.file_input
        steps = 100
        grid = AnimatedLightGrid(input)
        lit_lights = grid.animate(steps)
        return lit_lights

    @property
    def second(self):
        pass

    #
    # Tests
    #
    @property
    def test1(self):
        input = self.TEST_INPUT
        steps = 4

        grid = AnimatedLightGrid(input)
        neighbors = grid.neighbors((1, 3))
        lit_neighbors = [pt for pt in neighbors if grid.grid[pt] == '#']
        assert len(grid.pts) == 36, len(grid.pts)
        assert len(neighbors) == 8, neighbors
        assert len(lit_neighbors) == 4, lit_neighbors

        lit_lights = grid.animate(steps)
        assert lit_lights == 4, lit_lights

        return 'passed'

    @property
    def test2(self):
        input = self.TEST_INPUT
        print(input)
        return 'passed'

    #
    # Properties
    #
    @cached_property
    def file_input(self):
        with open(self.INPUT_FILE) as file:
            return file.read().strip()


#
# Main
#
puzzle = AdventPuzzle()
puzzle.solve()
