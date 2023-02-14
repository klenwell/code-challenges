"""
Advent of Code 2015 - Day 18
https://adventofcode.com/2015/day/18

Day 18: Like a GIF For Your Yard
"""
from os.path import join as path_join
from functools import cached_property
from common import INPUT_DIR, Grid, info


class AnimatedLightGrid(Grid):
    @property
    def lit_lights(self):
        return [pt for pt in self.pts if self.grid[pt] == '#']

    def animate(self, steps):
        for n in range(steps):
            info(f"step {n}", 10)
            grid = self.animate_step()
            self.grid = grid
        return len(self.lit_lights)

    def faulty_animate(self, steps):
        # four lights, one in each corner, are stuck on and can't be turned off
        for n in range(steps):
            info(f"step {n}", 10)
            self.grid = self.light_corners(self.grid)
            grid = self.animate_step()
            self.grid = grid
        self.grid = self.light_corners(self.grid)
        return len(self.lit_lights)

    def animate_step(self):
        next_grid = {}
        for pt in self.pts:
            value = self.animate_pt(pt)
            next_grid[pt] = value
        return next_grid

    def light_corners(self, grid):
        corner = {
            'nw': (self.min_x, self.min_y),
            'ne': (self.max_x, self.min_y),
            'se': (self.max_x, self.max_y),
            'sw': (self.min_x, self.max_y)
        }
        for pt in corner.values():
            grid[pt] = '#'
        return grid

    def animate_pt(self, pt):
        before = self.grid[pt]
        is_on = before == '#'
        neighbors_on = 0

        for npt in self.neighbors(pt):
            if self.grid[npt] == '#':
                neighbors_on += 1

        # A light which is on stays on when 2 or 3 neighbors are on, and turns off otherwise.
        if is_on:
            stays_on = neighbors_on in (2, 3)
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
        input = self.file_input
        steps = 100
        grid = AnimatedLightGrid(input)
        lit_lights = grid.faulty_animate(steps)
        return lit_lights

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
        steps = 5

        grid = AnimatedLightGrid(input)
        lit_lights = grid.faulty_animate(steps)

        assert lit_lights == 17, lit_lights
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
