"""
Advent of Code 2015 - Day 12
https://adventofcode.com/2015/day/12

Day 12: JSAbacusFramework.io
"""
from os.path import join as path_join
from functools import cached_property
from common import INPUT_DIR, extract_numbers, info
import json


class ElfAcctFile:
    def __init__(self, input):
        self.input = input.strip()

    @cached_property
    def sum(self):
        return sum(self.numbers)

    @cached_property
    def redless_sum(self):
        return sum(self.numbers_sans_red)

    @cached_property
    def numbers(self):
        return extract_numbers(self.input, num_type=int)

    @cached_property
    def numbers_sans_red(self):
        numbers = []
        discards = []
        queue = [ElfAcctEntry(json.loads(self.input))]

        while queue:
            entry = queue.pop(0)
            queue += entry.children
            numbers += entry.numbers
            discards += entry.discards
            info(f"{len(queue)} {len(numbers)} {len(discards)}", 40)

        return numbers


class ElfAcctEntry:
    def __init__(self, json_obj):
        self.type = type(json_obj)
        self.json_obj = json_obj

    @cached_property
    def sum(self):
        summed = sum(self.numbers)
        for child in self.children:
            summed += child.sum
        return summed

    @cached_property
    def values(self):
        if self.type == list:
            return self.json_obj
        elif self.type == dict:
            return self.json_obj.values()
        else:
            raise TypeError(f"Invalid Type: {self.type}")

    @cached_property
    def is_red(self):
        if self.type != dict:
            return False
        for value in self.values:
            if type(value) == str and value == 'red':
                return True
        return False

    @cached_property
    def numbers(self):
        numbers = []

        if self.is_red:
            return []

        for value in self.values:
            if type(value) == int:
                numbers.append(value)
        return numbers

    @cached_property
    def children(self):
        children = []

        if self.is_red:
            return []

        for value in self.values:
            if type(value) in (list, dict):
                entry = ElfAcctEntry(value)
                children.append(entry)
        return children

    @cached_property
    def discards(self):
        if self.is_red:
            return self.values

        discards = []

        for value in self.values:
            if type(value) not in (list, dict, int):
                discards.append(value)
        return discards


class DailyPuzzle:
    INPUT_FILE = path_join(INPUT_DIR, 'day-12.txt')

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
        acct_file = ElfAcctFile(input)
        return acct_file.sum

    @property
    def second(self):
        input = self.file_input
        acct_file = ElfAcctFile(input)
        entry = ElfAcctEntry(json.loads(input))

        assert acct_file.redless_sum == entry.sum, (acct_file.redless_sum, entry.sum)
        return entry.sum

    #
    # Tests
    #
    @property
    def test1(self):
        test_cases = [
            # input, sum
            ('[1,2,3]', 6),
            ('{"a":2,"b":4}', 6),
            ('[[[3]]]', 3),
            ('{"a":{"b":4},"c":-1}', 3),
            ('{"a":[-1,1]}', 0),
            ('[-1,{"a":1}]', 0),
            ('[]', 0),
            ('{}', 0),
        ]

        for input, expected in test_cases:
            acct_file = ElfAcctFile(input)
            assert acct_file.sum == expected, (input, acct_file.sum, expected)

        return 'passed'

    @property
    def test2(self):
        input = json.loads('{"d":"red","e":[1,2,3,4],"f":5}')
        entry = ElfAcctEntry(input)
        assert entry.is_red, entry
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
