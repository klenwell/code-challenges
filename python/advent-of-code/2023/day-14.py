"""
Advent of Code 2023 - Day 14
https://adventofcode.com/2023/day/14
"""
from os.path import join as path_join
from functools import cached_property
from common import INPUT_DIR

N = (0, -1)
S = (0, 1)
E = (1, 0)
W = (-1, 0)
ROCK = 'O'
CYCLES = 1000000000


class ReflectorDish:
    def __init__(self, input):
        self.rows = self.input_to_rows(input)

    @property
    def total_load(self):
        total_load = 0

        cols = list(self.cols)
        max_col = len(cols[0])

        for col in cols:
            for n, space in enumerate(col):
                if space == ROCK:
                    load = max_col - n
                    total_load += load
        return total_load

    @property
    def cols(self):
        cols = []
        for n in range(len(self.rows[0])):
            col = []
            for row in self.rows:
                val = row[n]
                col.append(val)
            cols.append(col)
        return cols

    def spin(self, cycles):
        cycle = 0
        loads = []

        while cycle < cycles:
            for dir in (N, W, S, E):
                self.tilt(dir)

            cycle += 1
            loads.append(self.total_load)

            if self.detect_pattern(loads):
                # fast forward
                cycles_left = cycles - cycle
                pattern_length = len(self.extract_pattern(loads))
                pattern_cycles = cycles_left // pattern_length
                skip_ahead = pattern_cycles * pattern_length
                cycle += skip_ahead

        return self

    def detect_pattern(self, loads):
        pattern = self.extract_pattern(loads)
        return pattern is not None

    def extract_pattern(self, loads):
        if len(loads) < 8:
            return None

        last_seg = loads[-4:]
        seq = loads[0:-4]
        haystack = seq[::-1]
        needle = last_seg[::-1]

        for n in range(0, len(haystack)-4):
            a, b = n, n+4
            segment = haystack[a:b]
            if needle == segment:
                pattern = haystack[0:n][::-1] + needle[::-1]
                return pattern

        return None

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
            self.rows = self.cols_to_rows(seqs)
        else:
            self.rows = seqs

        return self

    def tilt_seqs(self, seqs, d1):
        seqs_out = []
        for seq in seqs:
            seq_out = self.tilt_seq(seq, d1)
            seqs_out.append(seq_out)
        return seqs_out

    def tilt_seq(self, seq, d1):
        seq_out = ['.' for v in seq if v]
        stop = 0

        # Reverse if direction is positive (E or S). Tilt logic
        # below is leftward or backward.
        if d1 == 1:
            seq = seq[::-1]

        for n, space in enumerate(seq):
            if space == ROCK:
                seq_out[stop] = ROCK
                stop += 1
            elif space == '#':
                seq_out[n] = space
                stop = n + 1
            else:
                seq_out[n] = space

        # Now that tilting is done, unreverse reversed sequences
        if d1 == 1:
            seq_out = seq_out[::-1]

        return seq_out

    def input_to_rows(self, input):
        rows = []
        lines = input.strip().split('\n')
        for line in lines:
            row = list(line)
            rows.append(row)
        return rows

    def cols_to_rows(self, cols):
        rows = []
        max_y = len(cols[0])
        for y in range(max_y):
            row = []
            for col in cols:
                val = col[y]
                row.append(val)
            rows.append(row)
        return rows


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
        dish.tilt(N)
        assert dish.total_load == 110821, dish.total_load
        return dish.total_load

    @property
    def second(self):
        input = self.file_input
        dish = ReflectorDish(input)
        dish.spin(CYCLES)
        return dish.total_load

    #
    # Tests
    #
    @property
    def test1(self):
        input = self.TEST_INPUT
        dish = ReflectorDish(input)
        dish.tilt(N)
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

        dish.spin(CYCLES)
        assert dish.total_load == 64, dish.total_load
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
