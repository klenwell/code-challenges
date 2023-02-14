"""
Advent of Code 2015 - Day 19
https://adventofcode.com/2015/day/19

Day 19: Medicine for Rudolph
"""
from os.path import join as path_join
from functools import cached_property
from common import INPUT_DIR


class NorthPoleReactor:
    def __init__(self, input):
        self.input = input.strip()

    @cached_property
    def transforms(self):
        transforms = []
        lines, _ = self.input.split('\n\n')
        for line in lines.split('\n'):
            find, replace = line.split(' => ')
            transform = (find, replace)
            transforms.append(transform)
        return transforms

    @cached_property
    def molecule(self):
        _, molecule = self.input.split('\n\n')
        return molecule.strip()

    def calibrate(self):
        distinct_molecules = set()
        for transform in self.transforms:
            new_molecules = self.transform_molecule(transform)
            distinct_molecules = distinct_molecules.union(new_molecules)
        return distinct_molecules

    def transform_molecule(self, transform):
        print(transform, self.molecule)
        new_molecules = set()
        n = 0
        find, replace = transform
        find_len = len(find)
        for n in range(0, len(self.molecule)):
            seg_end = n+find_len
            segment = self.molecule[n:seg_end]
            print(segment, find)
            if segment == find:
                new_molecule = self.molecule[0:n] + replace + self.molecule[seg_end:]
                new_molecules.add(new_molecule)
        return new_molecules




class AdventPuzzle:
    INPUT_FILE = path_join(INPUT_DIR, 'day-19.txt')

    TEST_INPUT = """\
H => HO
H => OH
O => HH

HOH"""

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
        reactor = NorthPoleReactor(input)
        distinct_molecules = reactor.calibrate()
        return len(distinct_molecules)

    @property
    def second(self):
        pass

    #
    # Tests
    #
    @property
    def test1(self):
        input = self.TEST_INPUT
        reactor = NorthPoleReactor(input)
        assert reactor.transforms[0] == ('H', 'HO'), reactor.transforms
        assert reactor.molecule == 'HOH', reactor.molecule

        distinct_molecules = reactor.calibrate()
        assert len(distinct_molecules) == 4, distinct_molecules

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
puzzle = AdventPuzzle()
puzzle.solve()
