"""
Advent of Code 2022 - Day 20
https://adventofcode.com/2022/day/20
"""
from os.path import join as path_join
from functools import cached_property
from config import INPUT_DIR


INPUT_FILE = path_join(INPUT_DIR, 'day-20.txt')

TEST_INPUT = """\
1
2
-3
3
-2
0
4"""


class GroveFile:
    def __init__(self, input):
        self.input = [int(n) for n in input.split('\n')]
        self.mixed_sequence = self.input.copy()
        self.logs = [self.mixed_sequence]

    def decrypt(self):
        # Return coordinates
        self.mix()
        n1000 = self.value_at(0, 1000)
        n2000 = self.value_at(0, 2000)
        n3000 = self.value_at(0, 3000)
        return n1000 + n2000 + n3000

    def value_at(self, start, offset):
        start_index = self.mixed_sequence.index(start)
        new_index = start_index + offset
        max_index = len(self.mixed_sequence)
        print(start, offset, start_index, new_index)
        #print(self.mixed_sequence, new_index)

        if new_index >= max_index:
            new_index = new_index % max_index
        #print(new_index, self.mixed_sequence[new_index])

        return self.mixed_sequence[new_index]

    def mix(self):
        for n in self.input:
            self.mixed_sequence = self.move_in_sequence(n, self.mixed_sequence)
            self.logs.append(self.mixed_sequence)
            #print(n, self.mixed_sequence)
            #breakpoint()
        return self.mixed_sequence

    def move_in_sequence(self, n, sequence):
        old_index = sequence.index(n)
        new_index = old_index + n
        max_index = len(sequence)

        if new_index < 0:
            new_index = new_index % (max_index - 1)
        elif new_index > max_index:
            new_index = new_index % (max_index - 1)

        # The list is circular, so moving a number off one end of the list wraps back around
        # to the other end as if the ends were connected.
        if new_index == 0:
            new_index = max_index
        elif new_index == max_index - 1:
            new_index = 0

        old_seq = sequence.copy()
        old_seq.remove(n)
        new_seq = old_seq[:new_index] + [n] + old_seq[new_index:]
        return new_seq


class Solution:
    def __init__(self, input_file):
        self.input_file = input_file

    #
    # Solutions
    #
    @property
    def test1(self):
        input = TEST_INPUT

        self.test_move_in_sequence()
        self.test_mix()
        self.test_file_input()

        grove_file = GroveFile(input)
        sequence = grove_file.mix()
        assert sequence == [1, 2, -3, 4, 0, 3, -2], sequence
        assert grove_file.value_at(0, 1000) == 4, (grove_file.value_at(0, 1000), sequence)
        assert grove_file.value_at(0, 2000) == -3, (grove_file.value_at(0, 2000), sequence)
        assert grove_file.value_at(0, 3000) == 2, (grove_file.value_at(0, 3000), sequence)

        grove_file = GroveFile(input)
        sum = grove_file.decrypt()
        assert sum == 3, sum
        return sum

    def test_mix(self):
        expected_mixes = [
            [1, 2, -3, 3, -2, 0, 4],
            [2, 1, -3, 3, -2, 0, 4],
            [1, -3, 2, 3, -2, 0, 4],
            [1, 2, 3, -2, -3, 0, 4],
            [1, 2, -2, -3, 0, 3, 4],
            [1, 2, -3, 0, 3, 4, -2],
            [1, 2, -3, 0, 3, 4, -2],
            [1, 2, -3, 4, 0, 3, -2]
        ]

        grove_file = GroveFile(TEST_INPUT)
        sequence = grove_file.mix()

        for n, mix in enumerate(expected_mixes):
            assert grove_file.logs[n] == mix, (mix, expected_mixes)

        print('test_mix: passed')


    def test_file_input(self):
        input = self.file_input
        grove_file = GroveFile(input)
        sequence = grove_file.mixed_sequence

        assert len(sequence) == 5000, len(self.input_lines)
        assert sequence[0] == -9810, sequence[0]
        assert sequence[-1] == 4075, sequence[-1]

        print('test_file_input: passed')

    @property
    def first(self):
        input = self.file_input

        grove_file = GroveFile(input)
        sequence = grove_file.mix()
        at1000 = grove_file.value_at(0, 1000)
        at2000 = grove_file.value_at(0, 2000)
        at3000 = grove_file.value_at(0, 3000)
        print(grove_file.mixed_sequence.index(0), at1000, at2000, at3000)

        grove_file = GroveFile(input)
        sum = grove_file.decrypt()

        assert sum != -1295, 'wrong first answer'
        return sum

    @property
    def test2(self):
        pass

    @property
    def second(self):
        pass

    #
    # Tests
    #
    def test_move_in_sequence(self):
        test_cases = [
            (1, [4, 5, 6, 1, 7, 8, 9], [4, 5, 6, 7, 1, 8, 9]),
            (-2, [4, -2, 5, 6, 7, 8, 9], [4, 5, 6, 7, 8, -2, 9]),
            (2, [4, -2, 5, 6, 2, 8, 9], [2, 4, -2, 5, 6, 8, 9])
        ]
        grove_file = GroveFile('1')

        for n, seq, expected in test_cases:
            seq = grove_file.move_in_sequence(n, seq)
            assert seq == expected, (seq, expected)
        print('test_move_in_sequence: passed')

    #
    # Properties
    #
    @cached_property
    def file_input(self):
        with open(self.input_file) as file:
            return file.read().strip()

    @cached_property
    def input_lines(self):
        return [line.strip() for line in self.file_input.split("\n")]

    @cached_property
    def test_input_lines(self):
        return [line.strip() for line in TEST_INPUT.split("\n")]


#
# Main
#
solution = Solution(INPUT_FILE)
print("test 1 solution: {}".format(solution.test1))
print("pt 1 solution: {}".format(solution.first))
print("test 2 solution: {}".format(solution.test2))
print("pt 2 solution: {}".format(solution.second))
