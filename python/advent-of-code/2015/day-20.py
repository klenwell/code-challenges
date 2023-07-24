"""
Advent of Code 2015 - Day 20
https://adventofcode.com/2015/day/20
"""
from os.path import join as path_join
from functools import cached_property
from common import INPUT_DIR, compute_factors, info


class ElfDispatcher:
    def first_house_to_reach_gift_count(self, count):
        for n in range(1, count):
            gifts = self.count_gifts_for_house(n)
            info((n, gifts), 100000)
            if gifts >= count:
                return n

    def count_gifts_for_house(self, house_num):
        return sum(compute_factors(house_num)) * 10


class UnionizedElfDispatcher(ElfDispatcher):
    def count_gifts_for_house(self, house_num):
        elves = compute_factors(house_num)
        active_elves = [e for e in elves if house_num <= e * 50]
        return sum(active_elves) * 11


class AdventPuzzle:
    INPUT_FILE = path_join(INPUT_DIR, 'day-20.txt')

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
        input = 29000000
        dispatcher = ElfDispatcher()
        house_number = dispatcher.first_house_to_reach_gift_count(input)
        return house_number

    @property
    def second(self):
        input = 29000000
        dispatcher = UnionizedElfDispatcher()
        house_number = dispatcher.first_house_to_reach_gift_count(input)
        assert house_number < 718200, f"{house_number} is too high"
        return house_number

    #
    # Tests
    #
    @property
    def test1(self):
        input = 150
        dispatcher = ElfDispatcher()

        # Test count_gifts_for_house
        test_cases = [
            # house_num, expected
            (1, 10),
            (4, 70),
            (7, 80),
            (9, 130)
        ]
        for house_num, expected in test_cases:
            count = dispatcher.count_gifts_for_house(house_num)
            assert count == expected, (house_num, count, expected)

        # Test solution
        house_number = dispatcher.first_house_to_reach_gift_count(input)

        assert house_number == 8, house_number
        return 'passed'

    @property
    def test2(self):
        pass

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
