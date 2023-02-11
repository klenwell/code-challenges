"""
Advent of Code 2015 - Day 17
https://adventofcode.com/2015/day/17
"""
from os.path import join as path_join
from functools import cached_property
from common import INPUT_DIR, info


# Source: https://stackoverflow.com/a/71754403/1093087
def subset_sum(array, num):
    result = []

    def find(arr, num, path=()):
        info((arr, num, path), 20000)
        if not arr:
            return
        if arr[0] == num:
            result.append(path + (arr[0],))
        else:
            if num - arr[0] > 0:
                find(arr[1:], num - arr[0], path + (arr[0],))
        find(arr[1:], num, path)

    find(array, num)
    return result


class FridgeOrganizer:
    def __init__(self, container_sizes):
        self.container_sizes = container_sizes.strip()

    @cached_property
    def containers(self):
        containers = []
        for liters in self.container_sizes.split('\n'):
            container = int(liters)
            containers.append(container)
        return containers

    def count_combos(self, liters):
        return len(subset_sum(self.containers, liters))

    def count_min_containers(self, liters):
        combos = subset_sum(self.containers, liters)
        min_containers = self.find_min_containers(combos, liters)
        min_combos = [combo for combo in combos if len(combo) == min_containers]
        return len(min_combos)

    def find_min_containers(self, combos, liters):
        sorted_combos = [tuple(sorted(combo)) for combo in combos]
        combos_sorted_by_len = sorted(sorted_combos, key=lambda c: len(c))
        return len(combos_sorted_by_len[0])


class AdventPuzzle:
    INPUT_FILE = path_join(INPUT_DIR, 'day-17.txt')

    TEST_INPUT = """\
20
15
10
5
5"""

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
        organizer = FridgeOrganizer(input)
        num_combos = organizer.count_combos(150)
        return num_combos

    @property
    def second(self):
        input = self.file_input
        organizer = FridgeOrganizer(input)
        min_containers = organizer.count_min_containers(150)

        assert min_containers < 583, min_containers
        return min_containers

    #
    # Tests
    #
    @property
    def test1(self):
        target = 25
        input = self.TEST_INPUT
        containers = [int(n) for n in input.split('\n')]
        subsets = subset_sum(containers, target)
        assert len(subsets) == 4, subsets

        organizer = FridgeOrganizer(input)
        num_combos = organizer.count_combos(target)
        assert num_combos == 4, num_combos

        return 'passed'

    @property
    def test2(self):
        input = self.TEST_INPUT
        organizer = FridgeOrganizer(input)
        min_containers = organizer.count_min_containers(25)
        assert min_containers == 3, min_containers
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
