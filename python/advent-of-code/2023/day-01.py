"""
Advent of Code 2023 - Day 1
https://adventofcode.com/2023/day/1
"""
from os.path import join as path_join
from functools import cached_property
from common import INPUT_DIR


class Calibrator:
    def __init__(self, document):
        self.document = document

    @cached_property
    def sum(self):
        return sum(self.calibration_values)

    @property
    def calibration_values(self):
        for line in self.lines:
            yield self.restore_value(line)

    @cached_property
    def lines(self):
        return self.document.split("\n")

    def restore_value(self, line):
        digits = [c for c in line if c.isdigit()]
        return int(f'{digits[0]}{digits[-1]}')


class Recalibrator(Calibrator):
    def restore_value(self, line):
        words = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']

        for i, word in enumerate(words):
            if word in line:
                insert = f'{word}{str(i + 1)}{word}'
                line = line.replace(word, insert)

        digits = [c for c in line if c.isdigit()]
        return int(f'{digits[0]}{digits[-1]}')


class AdventPuzzle:
    INPUT_FILE = path_join(INPUT_DIR, 'day-01.txt')

    TEST_INPUT = """\
1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet"""

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
        calibrator = Calibrator(input)
        assert calibrator.sum == 54338
        return calibrator.sum

    @property
    def second(self):
        input = self.file_input
        calibrator = Recalibrator(input)
        assert calibrator.sum != 53340, 53340
        assert calibrator.sum == 53389, calibrator.sum
        return calibrator.sum

    #
    # Tests
    #
    @property
    def test1(self):
        input = self.TEST_INPUT
        calibrator = Calibrator(input)
        assert calibrator.sum == 142
        return 'passed'

    @property
    def test2(self):
        input = """\
two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen"""

        calibrator = Recalibrator(input)
        assert calibrator.sum == 281, calibrator.sum
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
