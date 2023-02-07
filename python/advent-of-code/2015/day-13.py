"""
Advent of Code 2015 - Day 13
https://adventofcode.com/2015/day/13

Day 13: Knights of the Dinner Table
"""
from os.path import join as path_join
from functools import cached_property
from common import INPUT_DIR, info
from itertools import permutations


class HolidayTable:
    def __init__(self, guest_list):
        self.guest_list = guest_list.strip()

    @cached_property
    def guests(self):
        guests = set()
        for line in self.guest_list.split('\n'):
            guest, tail = line.split(' would ')
            guests.add(guest)
        return guests

    @cached_property
    def affinities(self):
        affinities = {}
        for line in self.guest_list.split('\n'):
            guest, tail = line.split(' would ')
            affinity, tail = tail.split(' happiness ')
            delta, points = affinity.strip().split(' ')
            _, neighbor = tail.split('next to ')

            mult = 1 if delta == 'gain' else -1
            score = int(points.strip()) * mult
            neighbor = neighbor[:-1]

            affinities[(guest, neighbor)] = score
        return affinities

    @property
    def optimal_seating_arrangement(self):
        scores = []
        possible_arrangements = list(permutations(self.guests))
        for n, arrangement in enumerate(possible_arrangements):
            score = self.score_arrangement(arrangement)
            scores.append((score, arrangement))
            info(f"arrangement {n+1} of {len(possible_arrangements)}", 4000)
        return sorted(scores, reverse=True)[0]

    def score_arrangement(self, guests):
        happiness = 0
        for n, guest in enumerate(guests):
            left = guests[n-1] if n > 0 else guests[-1]
            right = guests[n+1] if n < len(guests)-1 else guests[0]
            left_score = self.affinities.get((guest, left), 0)
            right_score = self.affinities.get((guest, right), 0)
            happiness = happiness + left_score + right_score
        return happiness


class AdventPuzzle:
    INPUT_FILE = path_join(INPUT_DIR, 'day-13.txt')

    TEST_INPUT = """\
Alice would gain 54 happiness units by sitting next to Bob.
Alice would lose 79 happiness units by sitting next to Carol.
Alice would lose 2 happiness units by sitting next to David.
Bob would gain 83 happiness units by sitting next to Alice.
Bob would lose 7 happiness units by sitting next to Carol.
Bob would lose 63 happiness units by sitting next to David.
Carol would lose 62 happiness units by sitting next to Alice.
Carol would gain 60 happiness units by sitting next to Bob.
Carol would gain 55 happiness units by sitting next to David.
David would gain 46 happiness units by sitting next to Alice.
David would lose 7 happiness units by sitting next to Bob.
David would gain 41 happiness units by sitting next to Carol."""

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
        table = HolidayTable(input)
        happiness, _ = table.optimal_seating_arrangement
        return happiness

    @property
    def second(self):
        pass

    #
    # Tests
    #
    @property
    def test1(self):
        input = self.TEST_INPUT
        table = HolidayTable(input)
        happiness, _ = table.optimal_seating_arrangement
        assert happiness == 330, (happiness)
        return 'passed'

    @property
    def test2(self):
        input = self.TEST_INPUT
        #print(input)
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
