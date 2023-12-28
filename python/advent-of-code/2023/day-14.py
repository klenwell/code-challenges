"""
Advent of Code 2023 - Day 14
https://adventofcode.com/2023/day/14
"""
from os.path import join as path_join
from functools import cached_property
from common import INPUT_DIR, Grid

N = (0, -1)
S = (0, 1)
E = (1, 0)
W = (-1, 0)
ROCK = 'O'
CYCLES = 1000000000


class ReflectorDish:
    def __init__(self, input):
        self.grid = Grid(input)

    @cached_property
    def total_load(self):
        total_load = 0
        cols = list(self.grid.cols)
        cols = self.tilt_north(cols)
        for col in cols:
            col_load = sum([t.load for t in col if type(t) is Rock])
            total_load += col_load
        return total_load

    @cached_property
    def max_row(self):
        return self.grid.max_y + 1

    def spin(self, cycles):
        states = []
        for n in range(cycles):
            for dir in (N, W, S, E):
                self.tilt(dir)
            states.append(self.state)

            if self.detect_pattern(states):
                breakpoint()
        return

    def tilt(self, dir):
        dx, dy = dir

        if dx == 0:
            seqs = list(self.cols)
            d1 = dy
        else:
            seqs = list(self.rows)
            d1 = dx

        seqs = self.tilt_seqs(seqs, d1)

        if dx == 0:
            self.cols_to_pts(seqs)
        else:
            self.rows_to_pts(seqs)

        return self

    def tilt_seqs(self, seqs, d1):
        seqs_out = []
        for seq in seqs:
            seq_out = self.tilt_seq(self, seq, d1)
            seqs_out.append(seq_out)
        return seqs

    def tilt_seq(self, seq, d1):
        step = d1
        seq_out = ['.' for v in seq if v]
        stop = 0

        if d1 == 1:
            seq = seq[::-1]

        for n, space in enumerate(seq):
            if space == 'O':
                seq_out[stop] = ROCK
                stop += 1
            elif space == '#':
                seq_out[n] = space
                stop = n + 1
            else:
                seq_out[n] = space

        if d1 == 1:
            seq_out = seq_out[::-1]

        return seq_out

    def tilt_north(self, cols):
        cols_in = cols
        cols_out = []

        for x, col_in in enumerate(cols_in):
            col_out = self.tilt_col_north(col_in, x)
            cols_out.append(col_out)

        return cols_out

    def tilt_col_north(self, col_in, x):
        col_out = ['.' for _ in col_in]
        for y,  tile in enumerate(col_in):
            if tile != ROCK:
                col_out[y] = tile
                continue
            rock = Rock(x, y, self)
            rock.roll_north(col_out)
            col_out[rock.y] = rock
        #print(col_in, col_out)
        return col_out


class Rock:
    def __init__(self, x, y, dish):
        self.x = x
        self.y = y
        self.dish = dish

    @property
    def load(self):
        return self.dish.max_row - self.y

    def roll_north(self, terrain):
        i = self.y
        rolling = i > 0
        while rolling and i > 0:
            next_tile = terrain[i-1]
            rolling = next_tile == '.'
            if rolling:
                i -= 1
        self.y = i
        return self





class AdventPuzzle:
    INPUT_FILE = path_join(INPUT_DIR, 'day-14.txt')

    TEST_INPUT = """\
O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#...."""

    #
    # Solutions
    #
    @property
    def first(self):
        input = self.file_input
        dish = ReflectorDish(input)
        return dish.total_load

    @property
    def second(self):
        pass

    #
    # Tests
    #
    @property
    def test1(self):
        input = self.TEST_INPUT
        dish = ReflectorDish(input)
        assert dish.total_load == 136, dish.total_load
        return 'passed'

    @property
    def test2(self):
        input = self.TEST_INPUT
        dish = ReflectorDish(input)

        dx, _ = W
        seq_in = list('..O.#..OO.#')
        expect = list('O...#OO...#')
        seq_out = dish.tilt_seq(seq_in, dx)
        assert seq_out == expect, (seq_out, expect)

        dx, _ = E
        seq_in = list('..O.#..OO.#')
        expect = list('...O#...OO#')
        seq_out = dish.tilt_seq(seq_in, dx)
        assert seq_out == expect, (seq_out, expect)


        #dish.spin(CYCLES)
        #assert dish.total_load == 64, dish.total_load
        return 'passed'

    #
    # Etc...
    #
    @cached_property
    def file_input(self):
        with open(self.INPUT_FILE) as file:
            return file.read().strip()

    def solve(self):
        print(f"test 1 solution: {self.test1}")
        print(f"Part 1 Solution: {self.first}")
        print(f"test 2 solution: {self.test2}")
        print(f"Part 2 Solution: {self.second}")


#
# Main
#
puzzle = AdventPuzzle()
puzzle.solve()
