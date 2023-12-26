"""
Advent of Code 2023 - Day 13
https://adventofcode.com/2023/day/13
"""
from os.path import join as path_join
from functools import cached_property
from common import INPUT_DIR


class MirrorScape:
    def __init__(self, input):
        self.input = input.strip()

    @cached_property
    def pattern_sum(self):
        return 0

    @cached_property
    def patterns(self):
        patterns = []
        blocks = self.input.split('\n\n')
        for block in blocks:
            pattern = MirrorPattern(block)
            patterns.append(pattern)
        return patterns


class MirrorPattern:
    def __init__(self, input):
        self.input = input.strip()

    @cached_property
    def summary(self):
        sum = 0
        if self.vertical_reflection_pivot:
            sum += self.vertical_reflection_pivot
        if self.horizontal_line_of_reflection:
            sum += 100 * self.horizontal_line_of_reflection
        return sum

    @cached_property
    def vertical_reflection_pivot(self):
        return self.reflection_pivot(self.cols)
        max_x = len(self.cols)
        print(self.cols)
        for n, col in enumerate(self.cols[0:-1]):
            pivot = n+1
            ref_len = min(pivot, max_x-n-1)
            i0, i1 = pivot-ref_len, pivot
            m0, m1 = pivot, pivot+ref_len
            left_image = ''.join(c for c in self.cols[i0:i1])
            right_image = ''.join(c[::-1] for c in self.cols[m0:m1])
            print(n, pivot, ref_len, (i0, i1), left_image, (m0, m1), right_image)
            assert len(left_image) == len(right_image), (len(left_image), len(right_image))
            if left_image == right_image[::-1]:
                return pivot
        return False

    @cached_property
    def horizontal_reflection_pivot(self):
        return self.reflection_pivot(self.rows)

    def reflection_pivot(self, seq):
        max_n = len(seq)
        print(seq)
        for n, col in enumerate(seq[0:-1]):
            pivot = n+1
            ref_len = min(pivot, max_n-n-1)
            i0, i1 = pivot-ref_len, pivot
            m0, m1 = pivot, pivot+ref_len
            left_image = ''.join(c for c in seq[i0:i1])
            right_image = ''.join(c[::-1] for c in seq[m0:m1])
            print(n, pivot, ref_len, (i0, i1), left_image, (m0, m1), right_image)
            assert len(left_image) == len(right_image), (len(left_image), len(right_image))
            if left_image == right_image[::-1]:
                return pivot
        return False


    @cached_property
    def rows(self):
        rows = []
        lines = self.input.split('\n')
        for line in lines:
            row = line
            rows.append(row)
        return rows

    @cached_property
    def cols(self):
        cols = []
        for n, _ in enumerate(self.rows[0]):
            vals = []
            for row in self.rows:
                val = row[n]
                vals.append(val)
            col = ''.join(vals)
            cols.append(col)
        return cols


class AdventPuzzle:
    INPUT_FILE = path_join(INPUT_DIR, 'day-13.txt')

    TEST_INPUT = """\
#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#"""

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
        map = MirrorScape(input)

        vert_pattern = map.patterns[0]
        assert vert_pattern.vertical_reflection_pivot == 5, vert_pattern.vertical_reflection_pivot
        assert vert_pattern.horizontal_reflection_pivot == False

        horz_pattern = map.patterns[1]
        assert horz_pattern.vertical_reflection_pivot == False, horz_pattern.vertical_reflection_pivot
        assert horz_pattern.horizontal_reflection_pivot == 4, horz_pattern.horizontal_reflection_pivot

        assert map.pattern_sum == 405, map.pattern_sum
        return 'passed'

    @property
    def test2(self):
        input = self.TEST_INPUT
        print(input)
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
