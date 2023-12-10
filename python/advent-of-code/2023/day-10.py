"""
Advent of Code 2023 - Day 10
https://adventofcode.com/2023/day/10
"""
from os.path import join as path_join
from functools import cached_property
from common import INPUT_DIR, Grid


class PipeMaze(Grid):
    DIRS = {
        (0,-1): 'N',
        (1,0): 'E',
        (0,1): 'S',
        (-1,0): 'W'
    }

    @cached_property
    def steps_to_farthest_point(self):
        steps = []
        prev_pt = None
        pt = self.starting_pt
        back_at_start = False

        while not back_at_start:
            next_pt = self.move(pt, prev_pt)
            steps.append(next_pt)
            back_at_start = next_pt == self.starting_pt
            prev_pt = pt
            pt = next_pt

        return len(steps) / 2

    @cached_property
    def starting_pt(self):
        for pt, val in self.grid.items():
            if val == 'S':
                return pt
        raise Exception('starting pt not found!')

    def move(self, pt, prev_pt=None):
        if not prev_pt:
            return self.move_from_start_pt(pt)

        for npt in self.connected_pts(pt):
            if npt != prev_pt and npt in self.pts:
                print((pt, self.grid[pt]), (npt, self.grid[npt]))
                return npt

        raise Exception(f"Unable to move from pt {pt}")

    def connected_pts(self, pt):
        connections = {
            '|': ((0,-1), (0,1)),
            '-': ((-1,0), (1,0)),
            '7': ((-1,0), (0,1)),
            'F': ((0,1), (1,0)),
            'J': ((-1,0), (0,-1)),
            'L': ((0,-1), (1,0))
        }

        pts = []
        pipe = self.grid[pt]

        for dx, dy in connections[pipe]:
            nx = pt[0] + dx
            ny = pt[1] + dy
            npt = (nx, ny)
            pts.append(npt)

        return pts

    def pipes_connect(self, pipe1, pipe2):
        disconnects = {
            '|': '-',
            '-': '|',
            '7': '7',
            'F': 'F',
            'J': 'J',
            'L': 'L',
        }
        return disconnects[pipe1] != pipe2

    def move_from_start_pt(self, pt):
        valid_moves = {
            'N': ('|', '7', 'F'),
            'E': ('J', '7', '-'),
            'S': ('|', 'J', 'L'),
            'W': ('F', 'L', '-')
        }
        # Take first connect pt
        for npt in self.cardinal_neighbors(pt):
            dx = npt[0] - pt[0]
            dy = npt[1] - pt[1]

            dir = self.DIRS[(dx,dy)]
            val = self.grid[npt]

            print(pt, npt, dir, val, val in valid_moves[dir])

            if val in valid_moves[dir]:
                return npt

        raise Exception('First move failed!')


class AdventPuzzle:
    INPUT_FILE = path_join(INPUT_DIR, 'day-10.txt')

    TEST_INPUT = """\
..F7.
.FJ|.
SJ.L7
|F--J
LJ..."""

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
        return input

    @property
    def second(self):
        pass

    #
    # Tests
    #
    @property
    def test1(self):
        input = self.TEST_INPUT
        maze = PipeMaze(input)

        assert maze.starting_pt == (0, 2), maze.starting_pt

        assert maze.steps_to_farthest_point == 8, maze.steps_to_farthest_point
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
