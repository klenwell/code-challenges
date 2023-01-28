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
        if self.has_naughty_pair():
            return False

        # It contains at least three vowels (aeiou only)
        if not self.has_at_least_three_vowels():
            return False

        # It contains at least one letter that appears twice in a row
        return self.has_repeating_letter()

    def is_nice_v2(self):
        # It contains a pair of any two letters that appears at least twice in the string
        # without overlapping
        if not self.has_repeating_non_overlapping_pair():
            return False

        # It contains at least one letter which repeats with exactly one letter between them
        if not self.has_one_repeating_letter_with_letter_between():
            return False

        return True

    def has_naughty_pair(self):
        naughty_strings = ('ab', 'cd', 'pq', 'xy')
        for ns in naughty_strings:
            if ns in self.value:
                return True
        return False

    def has_at_least_three_vowels(self):
        vowels = list('aeiou')
        vowel_count = 0
        for vowel in vowels:
            vowel_count += self.value.count(vowel)
            if vowel_count >= 3:
                return True
        return False

    def has_repeating_letter(self):
        for n, chr in enumerate(self.value):
            if n == 0:
                continue
            prev = self.value[n-1]
            if chr == prev:
                return True
        return False

    def has_repeating_non_overlapping_pair(self):
        pairs = [('_', '_')]

        for n, chr in enumerate(self.value):
            if n == 0:
                continue

            prev = self.value[n-1]
            pair = (prev, chr)

            if pair in pairs and pair != pairs[-1]:
                return True

            pairs.append(pair)

        return False

    def has_one_repeating_letter_with_letter_between(self):
        for n, c3 in enumerate(self.value):
            if n < 2:
                continue

            c1 = self.value[n-2]
            c2 = self.value[n-1]

            if c3 == c1 and c3 != c2:
                return True

        return False


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
        nice_strings = []
        values = self.file_input.strip().split('\n')

        for value in values:
            if SantaString(value).is_nice_v2():
                nice_strings.append(value)

        return len(nice_strings)

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
        test_cases = [
            # value, nice?
            ('qjhvhtzxzqqjkmpb', True),
            ('xxyxx', True),
            ('uurcxstgmygtbstg', False),
            ('ieodomkazucvgmuy', False),
            ('aaa', False)
        ]

        for value, is_nice in test_cases:
            ss = SantaString(value)
            assert ss.is_nice_v2() == is_nice, (value, ss.is_nice_v2(), is_nice)

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
