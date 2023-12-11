"""
Advent of Code 2023 - Day 111
https://adventofcode.com/2023/day/11
"""
from os.path import join as path_join
from functools import cached_property
from common import INPUT_DIR, Grid


class CosmicMap(Grid):
    def __init__(self, input, expand_factor=2):
        self.expand_factor = expand_factor
        super().__init__(input)

    @cached_property
    def shortest_path_sum(self):
        sum = 0
        for g1, g2 in self.galaxy_pairs:
            distance = self.measure_distance(g1, g2)
            sum += distance
        return sum

    @cached_property
    def expanded_rows(self):
        rows = []
        for n, row in enumerate(self.rows):
            if '#' not in row:
                rows.append(n)
        return set(rows)

    @cached_property
    def expanded_cols(self):
        cols = []
        for n, col in enumerate(self.cols):
            if '#' not in col:
                cols.append(n)
        return set(cols)

    @cached_property
    def galaxies(self):
        galaxies = []
        for pt, val in self.grid.items():
            if val == '#':
                galaxy = Galaxy(pt)
                galaxies.append(galaxy)
        return galaxies

    @cached_property
    def galaxy_pairs(self):
        pairs = set()
        for i, g1 in enumerate(self.galaxies):
            for j, g2 in enumerate(self.galaxies):
                if g1 == g2:
                    continue
                n1, n2 = sorted([i, j])
                pairs.add((self.galaxies[n1], self.galaxies[n2]))
        return pairs

    def measure_distance(self, g1, g2):
        # Compute Manhattan distance
        dx = abs(g2.x - g1.x)
        dy = abs(g2.y - g1.y)

        min_x, max_x = sorted([g1.x, g2.x])
        min_y, max_y = sorted([g1.y, g2.y])

        # Add additional expansion factor
        # NB: y values maps to *rows* and x values to *columns*
        expanded_rows = [y for y in self.expanded_rows if min_y < y < max_y]
        expanded_cols = [x for x in self.expanded_cols if min_x < x < max_x]
        row_expansion = len(expanded_rows) * self.expand_factor - len(expanded_rows)
        col_expansion = len(expanded_cols) * self.expand_factor - len(expanded_cols)

        return dx + dy + row_expansion + col_expansion


class Galaxy:
    def __init__(self, pt):
        self.x = pt[0]
        self.y = pt[1]

    def shortest_distance_to(self, other):
        # Use Manhattan distance
        dx = abs(other.x - self.x)
        dy = abs(other.y - self.y)
        return dx + dy

    def __repr__(self):
        return f"<Galaxy x={self.x} y={self.y}>"


class AdventPuzzle:
    INPUT_FILE = path_join(INPUT_DIR, 'day-11.txt')

    TEST_INPUT = """\
...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#....."""

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
        grid = CosmicMap(input)
        assert grid.shortest_path_sum == 9965032, grid.shortest_path_sum
        return grid.shortest_path_sum

    @property
    def second(self):
        input = self.file_input
        expand_factor = 1000000
        grid = CosmicMap(input, expand_factor)
        return grid.shortest_path_sum

    #
    # Tests
    #
    @property
    def test1(self):
        input = self.TEST_INPUT
        grid = CosmicMap(input)

        assert grid.expanded_rows == set([3, 7]), grid.expanded_rows
        assert grid.expanded_cols == set([2, 5, 8]), grid.expanded_cols
        assert len(grid.galaxy_pairs) == 36, len(grid.galaxy_pairs)
        assert grid.shortest_path_sum == 374, grid.shortest_path_sum

        return 'passed'

    @property
    def test2(self):
        input = self.TEST_INPUT

        expand_factor = 10
        grid = CosmicMap(input, expand_factor)
        assert grid.shortest_path_sum == 1030, grid.shortest_path_sum

        expand_factor = 100
        grid = CosmicMap(input, expand_factor)
        assert grid.shortest_path_sum == 8410, grid.shortest_path_sum

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
