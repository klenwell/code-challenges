"""
Advent of Code 2015 - Day 3
https://adventofcode.com/2022/day/3

Day 3: Perfectly Spherical Houses in a Vacuum
"""
from os.path import join as path_join
from functools import cached_property
from common import INPUT_DIR


class Santa:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.houses = {self.pt: 1}

    @property
    def pt(self):
        return (self.x, self.y)

    @property
    def lucky_houses(self):
        return [pt for pt, v in self.houses.items() if v > 0]

    def deliver(self, input):
        for dir in input:
            self.move(dir)

            if self.pt in self.houses:
                self.houses[self.pt] += 1
            else:
                self.houses[self.pt] = 1

        return len(self.lucky_houses)

    def move(self, dir):
        if dir == '>':
            self.x += 1
        elif dir == '<':
            self.x -= 1
        elif dir == 'v':
            self.y += 1
        else:
            self.y -= 1
        return self


class TeamSanta:
    def __init__(self):
        self.santa = Santa()
        self.robo_santa = Santa()

    def deliver(self, input):
        for n, dir in enumerate(input):
            santa = self.santa if n % 2 == 0 else self.robo_santa

            santa.move(dir)

            if santa.pt in santa.houses:
                santa.houses[santa.pt] += 1
            else:
                santa.houses[santa.pt] = 1

        lucky_houses = set(self.santa.lucky_houses + self.robo_santa.lucky_houses)
        return len(lucky_houses)


class DailyPuzzle:
    INPUT_FILE = path_join(INPUT_DIR, 'day-03.txt')

    TEST_INPUT = """\
^v^v^v^v^v"""

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
        input = self.file_input.strip()
        santa = Santa()
        lucky_houses = santa.deliver(input)
        assert lucky_houses != 1794, lucky_houses
        return lucky_houses

    @property
    def second(self):
        input = self.file_input.strip()
        team = TeamSanta()
        lucky_houses = team.deliver(input)
        return lucky_houses

    #
    # Tests
    #
    @property
    def test1(self):
        test_cases = [
            # input, expected
            ('>', 2),
            ('^>v<', 4),
            (self.TEST_INPUT, 2)
        ]

        for input, expected in test_cases:
            santa = Santa()
            lucky_houses = santa.deliver(input)
            assert lucky_houses == expected, (input, lucky_houses, expected)

        return 'passed'

    @property
    def test2(self):
        test_cases = [
            # input, expected
            ('^v', 3),
            ('^>v<', 3),
            (self.TEST_INPUT, 11)
        ]

        for input, expected in test_cases:
            team = TeamSanta()
            lucky_houses = team.deliver(input)
            assert lucky_houses == expected, (input, lucky_houses, expected)

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
