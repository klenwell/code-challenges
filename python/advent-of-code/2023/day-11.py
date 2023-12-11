"""
Advent of Code 2023 - Day 111
https://adventofcode.com/2023/day/11
"""
from os.path import join as path_join
from functools import cached_property
from common import INPUT_DIR, Grid, info


class CosmicMap(Grid):
    def __init__(self, input):
        input = self.expand_space(input.strip())
        super().__init__(input)

    @cached_property
    def shortest_path_sum(self):
        sum = 0
        for g1, g2 in self.galaxy_pairs:
            distance = g1.shortest_distance_to(g2)
            sum += distance
        return sum

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
        pairs = []
        paired = []
        for i, g1 in enumerate(self.galaxies):
            for j, g2 in enumerate(self.galaxies):
                info(f"pairing galaxy {i} of {len(self.galaxies)}", 10000)
                if g1 == g2:
                    continue
                pair = tuple(sorted([i, j]))
                if pair not in paired:
                    paired.append(pair)
                    pairs.append((g1, g2))
        return pairs

    def expand_space(self, input):
        # Any rows or columns that contain no galaxies should all actually be twice as big.
        lines = input.split('\n')
        rows = [list(line) for line in lines]
        cols = self.rows_to_cols(rows)

        # Expand empty cols
        expanded = 0
        for n, col in enumerate(cols):
            if not self.is_empty_space(col):
                continue
            expanded += 1
            for row in rows:
                row.insert(n + expanded, '.')

        # Expand empty rows
        new_rows = []
        for row in rows:
            new_rows.append(''.join(row))
            if self.is_empty_space(row):
                new_rows.append(''.join(row))

        return '\n'.join(new_rows)

    def is_empty_space(self, array):
        return set(array) == set(['.'])

    def rows_to_cols(self, rows):
        cols = []
        for n in range(len(rows[0])):
            col = []
            for row in rows:
                val = row[n]
                col.append(val)
            cols.append(col)
        return cols


class Galaxy:
    def __init__(self, pt):
        self.x = pt[0]
        self.y = pt[1]

    def shortest_distance_to(self, other):
        # Use Manhattan distance
        dx = abs(other.x - self.x)
        dy = abs(other.y - self.y)
        return dx + dy


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
        return grid.shortest_path_sum

    @property
    def second(self):
        pass

    #
    # Tests
    #
    @property
    def test1(self):
        input = self.TEST_INPUT
        grid = CosmicMap(input)

        assert grid.max_x == 12, grid.max_x
        assert grid.max_y == 11, grid.max_y
        assert len(grid.galaxy_pairs) == 36, len(grid.galaxy_pairs)

        assert grid.shortest_path_sum == 374, grid.shortest_path_sum

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
