"""
Advent of Code 2023 - Day 6
https://adventofcode.com/2023/day/6
"""
from os.path import join as path_join
from functools import cached_property
from common import INPUT_DIR,  info


class Regatta:
    def __init__(self, input):
        self.input = input

    @property
    def lines(self):
        return self.input.strip().split("\n")

    @property
    def durations(self):
        line = self.lines[0]
        _, values = line.split(':')
        return [int(d) for d in values.strip().split()]

    @property
    def distances(self):
        line = self.lines[1]
        _, values = line.split(':')
        return [int(d) for d in values.strip().split()]

    @property
    def races(self):
        races = []
        for n, duration in enumerate(self.durations):
            distance = self.distances[n]
            race = Race(duration, distance)
            races.append(race)
        return races

    @property
    def margin_of_error(self):
        wins = 1
        for race in self.races:
            wins = wins * race.wins
        return wins


class Race:
    def __init__(self, duration, distance):
        self.duration = duration
        self.distance = distance

    @property
    def wins(self):
        wins = 0
        for charge_time in range(self.duration):
            info(f"{self} {charge_time}", 100000)
            if self.can_win(charge_time):
                wins += 1
        return wins

    def can_win(self, charge_time):
        v = charge_time
        t = self.duration - charge_time
        d = v * t
        return d > self.distance

    def __repr__(self):
        return f"<Race t={self.duration} d={self.distance}>"




class AdventPuzzle:
    INPUT_FILE = path_join(INPUT_DIR, 'day-06.txt')

    TEST_INPUT = """\
Time:      7  15   30
Distance:  9  40  200"""

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
        regatta = Regatta(input)
        return regatta.margin_of_error

    @property
    def second(self):
        input = """\
Time:      41667266
Distance:  244104712281040"""
        regatta = Regatta(input)
        return regatta.margin_of_error

    #
    # Tests
    #
    @property
    def test1(self):
        input = """\
Time:      71530
Distance:  940200"""
        regatta = Regatta(input)
        return regatta.margin_of_error

    @property
    def test2(self):
        input = """\
Time:      71530
Distance:  940200"""
        regatta = Regatta(input)
        assert regatta.margin_of_error == 71503, regatta.margin_of_error
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
