"""
Advent of Code 2015 - Day 5
https://adventofcode.com/2022/day/5
"""
from os.path import join as path_join
from functools import cached_property
from common import INPUT_DIR


class SantaString:
    def __init__(self, value):
        self.value = value

    def is_nice(self):
        # It does not contain the strings ab, cd, pq, or xy
        naughty_strings = ('ab', 'cd', 'pq', 'xy')
        for ns in naughty_strings:
            if ns in self.value:
                return False

        # It contains at least three vowels (aeiou only)
        vowels = list('aeiou')
        vowel_count = 0
        for vowel in vowels:
            vowel_count += self.value.count(vowel)
            if vowel_count >= 3:
                break
        if vowel_count < 3:
            return False

        # It contains at least one letter that appears twice in a row
        chr_twice_in_row = False
        for n, chr in enumerate(self.value):
            if n == 0:
                continue
            prev_chr = self.value[n-1]
            if chr == prev_chr:
                chr_twice_in_row = True
                break
        if not chr_twice_in_row:
            return False

        return True


class DailyPuzzle:
    INPUT_FILE = path_join(INPUT_DIR, 'day-05.txt')

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
        nice_strings = []
        values = self.file_input.strip().split('\n')

        for value in values:
            if SantaString(value).is_nice():
                nice_strings.append(value)

        return len(nice_strings)


    @property
    def second(self):
        pass

    #
    # Tests
    #
    @property
    def test1(self):
        test_cases = [
            # value, nice?
            ('ugknbfddgicrmopn', True),
            ('aaa', True),
            ('jchzalrnumimnmhp', False),
            ('haegwjzuvuyypxyu', False),
            ('dvszwmarrgswjxmb', False)
        ]

        for value, is_nice in test_cases:
            santa_string = SantaString(value)
            assert santa_string.is_nice() == is_nice, (value, santa_string.is_nice(), is_nice)

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
