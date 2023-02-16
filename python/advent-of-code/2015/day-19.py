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
    def mutations(self):
        mutations = []
        lines, _ = self.input.split('\n\n')
        for line in lines.split('\n'):
            find, replace = line.split(' => ')
            mutation = (find, replace)
            mutations.append(mutation)
        return mutations

    @cached_property
    def mutation_map(self):
        map = {}
        for mutation in self.mutations:
            find, replace = mutation
            if find in map:
                map[find].append(replace)
            else:
                map[find] = [replace]
        return map

    @cached_property
    def molecule(self):
        _, code = self.input.split('\n\n')
        return Molecule(code)

    @cached_property
    def longest_transform(self):
        transforms = [t[1] for t in self.transforms]
        return sorted(transforms, key=lambda t: len(t))[-1]

    def calibrate(self, molecule):
        distinct_mutants = set()
        for mutation in self.mutations:
            mutants = molecule.mutate(mutation)
            distinct_mutants = distinct_mutants.union(mutants)
        return distinct_mutants

    def mutate_molecule(self, mutation, molecule):
        mutants = set()
        n = 0
        find, replace = transform
        find_len = len(find)
        for n in range(len(molecule)-find_len+1):
            seg_end = n+find_len
            segment = molecule[n:seg_end]
            info(f"{find} {segment}", 1000000)
            if segment == find:
                mutants = molecule[0:n] + replace + molecule[seg_end:]
                mutants.add(new_molecule)
        return new_molecules

    def mutate(self, rna, molecule):
        mutants = []
        start_at = rna.deviates_at(molecule)
        #print(start_at, rna.code, molecule)
        mutations = self.mutate_at(rna.code, start_at)
        for mutation in mutations:
            mutant = rna.clone()
            mutant.mutate(mutation)
            mutants.append(mutant)
            #print(mutant)
        return mutants

    def mutate_at(self, code, index):
        distinct_mutants = set()
        for transform in self.transforms:
            mutants = self.transform_rna_at(transform, code, index)
            distinct_mutants = distinct_mutants.union(mutants)
        return distinct_mutants

    def transform_rna_at(self, transform, code, index):
        mutants = set()
        n = 0
        find, replace = transform
        find_len = len(find)
        end = len(code)-find_len+1
        start = index
        for n in range(start, end):
            seg_end = n+find_len
            segment = code[n:seg_end]
            info(f"{find} {segment}", 1000000)
            if segment == find:
                mutant = code[0:n] + replace + code[seg_end:]
                mutants.add(mutant)
        return mutants

    def clone_molecule(self, molecule):
        cloned = []
        discards = []
        queue = [ReindeerNucleicAcid('e')]
        quickest = None
        leader = None

        while queue:
            rna = queue.pop(0)
            mutants = self.mutate(rna, molecule)

            for mutant in mutants:
                if mutant.clones(molecule):
                    cloned.append(mutant)
                    if not quickest or mutant.steps < quickest.steps:
                        quickest = mutant
                elif quickest and quickest.steps < mutant.steps:
                    discards.append(mutant.code)
                elif leader:
                    if mutant.transcribes(molecule) and \
                        mutant.head_size(molecule) >= leader.head_size(molecule):
                        leader = mutant
                        queue.append(mutant)
                    else:
                        discards.append(mutant)
                else:
                    if mutant.transcribes(molecule):
                        leader = clone
                    queue.append(clone)

            info((len(queue), len(discards), len(cloned), rna, quickest), 1000)

        info(f"quickest: {quickest.steps} ({len(queue)}, {len(cloned)})")
        return quickest.steps

    def mutant_is_dead_end(self, rna, molecule):
        deviates_at = rna.deviates_at(molecule)
        tail_deviation = len(rna.code) - deviates_at
        return tail_deviation > len(self.longest_transform)

    def fabricate_molecule(self, code):
        molecule = FabricatedMolecule(code)
        fabricated = []
        discards = []
        queue = [FabricatedMolecule('e')]
        quickest = None
        leader = None

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
                elif leader:
                    if not clone.transcribes(molecule):
                        discards.append(clone)
                        continue
                    if clone.head_size(molecule) < leader.head_size(molecule):
                        discards.append(clone)
                        continue
                    leader = clone
                    queue.append(clone)
                else:
                    if clone.transcribes(molecule):
                        leader = clone
                        #breakpoint()
                    queue.append(clone)

            info((len(queue), len(discards), len(fabricated), fab, leader), 1000)

        info(f"quickest: {quickest.steps} ({len(queue)}, {len(fabricated)})")
        return quickest.steps


class Molecule:
    def __init__(self, code):
        self.code = code.strip()

    @property
    def length(self):
        return len(self.code)

    def mutate(self, mutation):
        mutants = set()
        n = 0
        find, replace = mutation
        find_len = len(find)
        for n in range(self.length-find_len+1):
            seg_end = n+find_len
            segment = self.code[n:seg_end]
            info(f"{find} {segment}", 1000000)
            if segment == find:
                mutant = self.code[0:n] + replace + self.code[seg_end:]
                mutants.add(mutant)
        return mutants

    def __repr__(self):
        return f"<Molecule code={self.code}>"


class ReindeerNucleicAcid:
    def __init__(self, code):
        self.mutations = [code.strip()]

    @property
    def code(self):
        return self.mutations[-1]

    @property
    def steps(self):
        return len(self.mutations) - 1

    def deviates_at(self, code):
        """
        Returns index at which code deviates.

        Where self = 'abc' and other = 'adef', size would be 1
        Where self = 'abc' and other = 'abee', size would be 3
        Where self = 'bca' and other = 'abc', size would be 0
        """
        for n, chr in enumerate(self.code):
            if chr != code[n]:
                return n
        return n + 1

    def mutate(self, new_code):
        self.mutations.append(new_code)
        return self

    def clone(self):
        clone = ReindeerNucleicAcid(self.code)
        clone.mutations = self.mutations.copy()
        return clone

    def clones(self, code):
        return self.code == code

    def __repr__(self):
        return f"<RNA steps={self.steps} {self.code}>"


class FabricatedMolecule:
    def __init__(self, code):
        self.transforms = [code]

    @property
    def latest(self):
        return self.transforms[-1]

    @property
    def length(self):
        return len(self.transforms[-1])

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

    def transcribes(self, other):
        if not self.heads(other):
            return False

        if self.tail_deviates(other):
            return False

        return True

    def heads(self, other):
        return self.head_size(other) > 0

    def head_size(self, other):
        """
        Returns length of head matching "other" molecule head.

        Where self = 'abc' and other = 'adef', size would be 1 for 'a'
        Where self = 'abc' and other = 'abee', size would be 2 for 'ab'
        Where self = 'bca' and other = 'abc', size would be 0
        """
        for n, chr in enumerate(self.latest):
            if chr != other.latest[n]:
                return n
        return n + 1

    def tail_deviates(self, other):
        max_deviance = 10
        start = self.length-1
        end = -1
        step = -1

        deviants = 0
        for n in range(start, end, step):
            self_chr = self.latest[n]
            other_chr = other.latest[n]
            if self_chr != other_chr:
                deviants += 1
            if deviants > max_deviance:
                return True
        return False

    def starts_for(self, other):
        if other.latest.startswith(self.latest):
            return self.length
        else:
            return 0

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
        input = self.file_input
        reactor = NorthPoleReactor(input)
        min_steps = reactor.clone_molecule(reactor.molecule)
        return min_steps

    #
    # Tests
    #
    @property
    def test1(self):
        input = self.TEST_INPUT
        reactor = NorthPoleReactor(input)
        molecule = reactor.molecule
        assert reactor.mutations[0] == ('H', 'HO'), reactor.mutations
        assert molecule.code == 'HOH', molecule

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
        min_steps = reactor.clone_molecule(reactor.molecule)
        assert min_steps == 3, min_steps

        #self.test_heads()

        return 'passed'

    def test_heads(self):
        target = FabricatedMolecule('abcdef')
        test_cases = [
            # code, size
            ('abc', 3),
            ('abce', 3),
            ('bcd', 0)
        ]

        for code, expected in test_cases:
            m = FabricatedMolecule(code)
            size = m.head_size(target)
            assert size == expected, m

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
