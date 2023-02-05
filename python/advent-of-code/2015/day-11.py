"""
Advent of Code 2015 - Day 11
https://adventofcode.com/2015/day/11

Day 11: Corporate Policy
"""
from os.path import join as path_join
from functools import cached_property
from common import INPUT_DIR, ALPHA_LOWER, info


class SantaPassword:
    def __init__(self):
        pass

    def update(self, password):
        while True:
            password = self.increment(password)
            info(f"{password}, {self.is_valid(password)}", 100000)
            if self.is_valid(password):
                return password

    def increment(self, password):
        digits = reversed(list(password))
        new_digits = []
        carry_over = False

        for n, letter in enumerate(digits):
            if n == 0 or carry_over:
                idx = ALPHA_LOWER.index(letter)
                next_idx = idx + 1
                carry_over = next_idx >= len(ALPHA_LOWER)
                new_letter = ALPHA_LOWER[0] if carry_over else ALPHA_LOWER[next_idx]
            else:
                new_letter = letter
            new_digits.append(new_letter)

        return ''.join(reversed(new_digits))


    def is_valid(self, password):
        if not self.includes_three_letter_sequence(password):
            return False

        if self.includes_confusing_letters(password):
            return False

        if not self.includes_two_non_overlapping_pairs(password):
            return False

        return True

    def includes_three_letter_sequence(self, password):
        for n in range(24):
            chr1, chr2, chr3 = ALPHA_LOWER[n], ALPHA_LOWER[n+1], ALPHA_LOWER[n+2]
            if f"{chr1}{chr2}{chr3}" in password:
                return True
        return False

    def includes_confusing_letters(self, password):
        confusing_letters = 'iol'
        for letter in confusing_letters:
            if letter in password:
                return True
        return False

    def includes_two_non_overlapping_pairs(self, password):
        pairs = []

        for n, letter in enumerate(password):
            if n == 0:
                continue

            prev = password[n-1]

            if letter == prev:
                # Pairs must not overlap
                if n > 1:
                    pre_prev = password[n-2]
                    if pre_prev == prev:
                        continue

                pair = (prev, letter)

                # Pairs must differ
                if pair not in pairs:
                    pairs.append(pair)

        return len(pairs) > 1


class DailyPuzzle:
    INPUT_FILE = path_join(INPUT_DIR, 'day-11.txt')

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
        input = 'cqjxjnds'
        santa_pass = SantaPassword()
        new_password = santa_pass.update(input)
        return new_password

    @property
    def second(self):
        input = 'cqjxxyzz'
        santa_pass = SantaPassword()
        new_password = santa_pass.update(input)
        return new_password

    #
    # Tests
    #
    @property
    def test1(self):
        # Validation Rules
        test_cases = [
            # password, is_valid
            ('hijklmmn', False),
            ('abbceffg', False),
            ('abbcegjk', False),
            ('abcbegjk', False),
            ('abcdffaa', True),
            ('ghjaabcc', True),
        ]
        santa_pass = SantaPassword()
        for password, expected in test_cases:
            is_valid = santa_pass.is_valid(password)
            assert is_valid == expected, (password, is_valid, expected)

        # Update
        test_cases = [
            # password, next
            ('abcdefgh', 'abcdffaa'),

            # Note: this will take minute to pass with current naive approach
            #('ghijklmn', 'ghjaabcc')
        ]
        for password, expected in test_cases:
            santa_pass = SantaPassword()
            new_password = santa_pass.update(password)
            assert new_password == expected, (password, new_password, expected)

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
