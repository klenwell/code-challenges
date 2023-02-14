"""
Advent of Code 2015 - Day 19
https://adventofcode.com/2015/day/19

Day 19: Medicine for Rudolph
"""
from os.path import join as path_join
from functools import cached_property
from common import INPUT_DIR, info


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

    @cached_property
    def transform_map(self):
        map = {}
        for transform in self.transforms:
            find, replace = transform
            if find in map:
                map[find].append(replace)
            else:
                map[find] = [replace]
        return map

    def calibrate(self, molecule):
        distinct_molecules = set()
        for transform in self.transforms:
            new_molecules = self.transform_molecule(transform, molecule)
            distinct_molecules = distinct_molecules.union(new_molecules)
        return distinct_molecules

    def transform_molecule(self, transform, molecule):
        new_molecules = set()
        n = 0
        find, replace = transform
        find_len = len(find)
        for n in range(0, len(molecule)):
            seg_end = n+find_len
            segment = molecule[n:seg_end]
            info(f"{find} {segment}", 1000)
            if segment == find:
                new_molecule = molecule[0:n] + replace + molecule[seg_end:]
                new_molecules.add(new_molecule)
        return new_molecules

    def fabricate_molecule(self, code):
        molecule = FabricatedMolecule(code)
        fabricated = []
        discards = []
        queue = [FabricatedMolecule('e')]
        quickest = None

        while queue:
            fab = queue.pop(0)
            clones = fab.react(self)

            for clone in clones:
                if clone.matches(molecule):
                    fabricated.append(clone)
                    if not quickest or clone.steps < quickest.steps:
                        quickest = clone
                elif quickest and quickest.steps < clone.steps:
                    discards.append(clone)
                else:
                    queue.append(clone)

            info(f"{len(queue)}, {len(fabricated)}, {quickest if quickest else ''}", 1000)

        info(f"quickest: {quickest.steps} ({len(queue)}, {len(fabricated)})")
        return quickest.steps


class FabricatedMolecule:
    def __init__(self, code):
        self.transforms = [code]

    @property
    def latest(self):
        return self.transforms[-1]

    @property
    def steps(self):
        return len(self.transforms) - 1

    def react(self, reactor):
        molecules = set()
        new_codes = reactor.calibrate(self.latest)
        for new_code in new_codes:
            clone = self.clone()
            clone.transform(new_code)
            molecules.add(clone)
        return molecules

    def transform(self, new_code):
        self.transforms.append(new_code)
        return self

    def clone(self):
        clone = FabricatedMolecule(self.transforms[0])
        clone.transforms = self.transforms.copy()
        return clone

    def matches(self, other):
        return self.latest == other.latest

    def __repr__(self):
        return f"<Molecule steps={self.steps} {self.latest}>"


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
        distinct_molecules = reactor.calibrate(reactor.molecule)
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

        distinct_molecules = reactor.calibrate(reactor.molecule)
        assert len(distinct_molecules) == 4, distinct_molecules

        return 'passed'

    @property
    def test2(self):
        input = """\
e => H
e => O
H => HO
H => OH
O => HH

HOH
"""
        reactor = NorthPoleReactor(input)
        min_steps = reactor.fabricate_molecule(reactor.molecule)
        assert min_steps == 3, min_steps
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
