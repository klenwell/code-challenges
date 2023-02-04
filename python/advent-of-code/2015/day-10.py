"""
Advent of Code 2015 - Day 10
https://adventofcode.com/2015/day/10

Day 10: Elves Look, Elves Say
"""
from os.path import join as path_join
from functools import cached_property
from common import INPUT_DIR, info


class LookSayingElf:
    def __init__(self):
        pass

    def chain_say_len(self, number, times):
        return len(self.chain_say(number, times))

    def chain_say(self, number, times):
        for n in range(times):
            number = self.say(number)
            info(f"{n} {len(number)}", 5)
        return number

    def say(self, number):
        spoken = []
        sequence = []

        for n, digit in enumerate(number):
            if n == 0:
                sequence.append(digit)
                continue

            last_digit = number[n-1]

            # Same sequence
            if digit == last_digit:
                sequence.append(digit)

            # New sequence
            else:
                num_digits = len(sequence)
                spoken += [str(num_digits), last_digit]
                sequence = [digit]

        # Don't forget the next sequence
        num_digits = len(sequence)
        spoken += [str(num_digits), digit]

        return ''.join(spoken)


class DailyPuzzle:
    INPUT_FILE = path_join(INPUT_DIR, 'day-10.txt')

    TEST_INPUT = """\
"""

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
        elf = LookSayingElf()
        return elf.chain_say_len('3113322113', 40)

    @property
    def second(self):
        input = self.file_input
        elf = LookSayingElf()
        return elf.chain_say_len('3113322113', 50)

    #
    # Tests
    #
    @property
    def test1(self):
        test_cases = [
            # input, expected, expected_len
            ('1', '11', 2),
            ('11', '21', 2),
            ('21', '1211', 4),
            ('1211', '111221', 6),
            ('111221', '312211', 6)
        ]
        for look, expected, expected_len in test_cases:
            elf = LookSayingElf()
            said = elf.say(look)
            assert said == expected, (look, said, expected)
            assert len(said) == expected_len, (look, len(said), expected_len)

        elf = LookSayingElf()
        said = elf.chain_say('1', 5)
        answer = elf.chain_say_len('1', 5)
        assert said == '312211', said
        assert answer == 6, answer

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
problem = DailyPuzzle()
problem.solve()
