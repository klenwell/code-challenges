"""
Advent of Code 2023 - Day 1
https://adventofcode.com/2023/day/1
"""
from os.path import join as path_join
from functools import cached_property
from common import INPUT_DIR, extract_numbers


class AdventPuzzle:
    INPUT_FILE = path_join(INPUT_DIR, 'day-01.txt')

    TEST_INPUT = """\
1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet"""

    def compute(self, input):
        strs = input.split("\n")
        sum = 0

        for s in strs:
            n = [int(s) for s in s if s.isdigit()]
            num = f'{n[0]}{n[-1]}'
            sum += int(num)
            print(n, num, sum)

        return sum
    
    def str_to_digits(self, s):
        word_nums = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']

        for n, wn in enumerate(word_nums):
            if wn in s:
                insert = f'{wn}{str(n + 1)}{wn}'
                s = s.replace(wn, insert)
        
        n = [int(s) for s in s if s.isdigit()]
        return int(f'{n[0]}{n[-1]}')
    
    def part2(self, input):
        strs = input.split("\n")
        sum = 0

        for s in strs:
            num = self.str_to_digits(s)
            #print(s, num)
            sum += num

        return sum

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
        sum = self.compute(input)
        return sum

    @property
    def second(self):
        input = self.file_input
        sum = self.part2(input)
        assert sum != 53340, 53340
        return sum

    #
    # Tests
    #
    @property
    def test1(self):
        input = self.TEST_INPUT
        print(input)
        sum = self.compute(input)
        assert sum == 142
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
        sum = self.part2(input)
        assert sum == 281, sum
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
