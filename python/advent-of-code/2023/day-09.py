"""
Advent of Code 2023 - Day 9
https://adventofcode.com/2023/day/9
"""
from os.path import join as path_join
from functools import cached_property
from common import INPUT_DIR


class Sensor:
    def __init__(self, report):
        self.report = report.strip()

    @cached_property
    def lines(self):
        return self.report.split("\n")

    @cached_property
    def next_values_sum(self):
        values = []
        for line in self.lines:
            extrapolator = Extrapolator(line)
            values.append(extrapolator.next_value)
        return sum(values)

    @cached_property
    def prev_values_sum(self):
        values = []
        for line in self.lines:
            extrapolator = Extrapolator(line)
            values.append(extrapolator.previous_value)
        return sum(values)


class Extrapolator:
    def __init__(self, input):
        self.input = input.strip()

    @cached_property
    def next_value(self):
        next_value = 0
        for sequence in self.sequences[1:]:
            last_value = sequence[-1]
            next_value += last_value
            # print(sequence, next_value)
        return next_value

    @cached_property
    def previous_value(self):
        prev_value = 0
        for sequence in self.sequences[1:]:
            first_value = sequence[0]
            prev_value = first_value - prev_value
            # print(prev_value, sequence)
        return prev_value

    @cached_property
    def history(self):
        return [int(n) for n in self.input.split()]

    @cached_property
    def sequences(self):
        sequence = list(self.history)
        sequences = [sequence]
        while set(sequence) != set([0]):
            sequence = self.derive_sequence(sequence)
            sequences.append(sequence)
        return list(reversed(sequences))

    def derive_sequence(self, sequence):
        derived = []
        for n, value in enumerate(sequence):
            if n == 0:
                continue
            diff = value - sequence[n-1]
            derived.append(diff)
        return derived


class AdventPuzzle:
    INPUT_FILE = path_join(INPUT_DIR, 'day-09.txt')

    TEST_INPUT = """\
0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45"""

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
        sensor = Sensor(input)
        return sensor.next_values_sum

    @property
    def second(self):
        input = self.file_input
        sensor = Sensor(input)
        return sensor.prev_values_sum

    #
    # Tests
    #
    @property
    def test1(self):
        input = self.TEST_INPUT
        sensor = Sensor(input)
        assert sensor.next_values_sum == 114, sensor.next_values_sum
        return 'passed'

    @property
    def test2(self):
        input = self.TEST_INPUT
        sensor = Sensor(input)
        assert sensor.prev_values_sum == 2, sensor.prev_values_sum
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
