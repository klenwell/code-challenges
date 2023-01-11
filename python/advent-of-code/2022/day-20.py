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
        self.input = [(i, int(n)) for i, n in enumerate(input.split('\n'))]
        self.indexed_sequence = self.input.copy()
        self.logs = [self.mixed_sequence]

    @property
    def mixed_sequence(self):
        return [n for _, n in self.indexed_sequence]

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
        #print(start, offset, start_index, new_index)

        if new_index >= max_index:
            new_index = new_index % max_index
        #print(new_index, self.mixed_sequence[new_index])

        return self.mixed_sequence[new_index]

    def mix(self):
        for i, n in self.input:
            self.indexed_sequence = self.move_in_sequence((i, n), self.indexed_sequence)
            self.logs.append(self.mixed_sequence)
            #print(n, self.mixed_sequence)
            #breakpoint()
        return self.mixed_sequence

    def move_in_sequence(self, val, sequence):
        _, n = val
        old_index = sequence.index(val)
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
        old_seq.remove(val)
        new_seq = old_seq[:new_index] + [val] + old_seq[new_index:]
        return new_seq


class EncryptedGroveFile(GroveFile):
    def __init__(self, input, key):
        super().__init__(input)
        self.input = [(i, n * key) for i, n in self.input]
        self.indexed_sequence = self.input.copy()
        self.logs = [self.mixed_sequence]

    def mix(self):
        # you need to mix the list of numbers ten times
        for n in range(10):
            print('Mix round:', n+1)
            super().mix()
        return self.mixed_sequence


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

    @property
    def first(self):
        input = self.file_input
        grove_file = GroveFile(input)
        sum = grove_file.decrypt()

        assert sum != -1295, 'wrong first answer'
        return sum

    @property
    def test2(self):
        input = TEST_INPUT
        key = 811589153

        grove_file = EncryptedGroveFile(input, key)
        sum = grove_file.decrypt()

        assert sum == 1623178306, sum
        return sum

    @property
    def second(self):
        input = self.file_input
        key = 811589153

        grove_file = EncryptedGroveFile(input, key)
        sum = grove_file.decrypt()
        return sum

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
            idx_seq = [(i, v) for i, v in enumerate(seq)]
            n_idx = seq.index(n)
            seq = grove_file.move_in_sequence((n_idx, n), idx_seq)
            unindexed_seq = [n for _, n in seq]
            assert unindexed_seq == expected, (unindexed_seq, expected)
        print('test_move_in_sequence: passed')

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
        deduplicated = list(set(sequence))

        assert len(sequence) == 5000, len(self.input_lines)
        assert sequence[0] == -9810, sequence[0]
        assert sequence[-1] == 4075, sequence[-1]
        assert len(deduplicated) != len(sequence), "expecting NOT same length"

        print('test_file_input: passed')

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
