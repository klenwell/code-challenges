"""
Advent of Code 2015 - Day 19
https://adventofcode.com/2015/day/19

Day 19: Medicine for Rudolph
"""
from os.path import join as path_join
from functools import cached_property
from queue import PriorityQueue
from functools import total_ordering
import random
from common import INPUT_DIR, info


class NorthPoleReactor:
    def __init__(self, input):
        self.input = input.strip()
        self.rna_registry = {}

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
    def molecule(self):
        _, code = self.input.split('\n\n')
        return Molecule(code)

    @cached_property
    def longest_mutation(self):
        mutations = [m[1] for m in self.mutations]
        return sorted(mutations, key=lambda m: len(m))[-1]

    def calibrate(self, molecule):
        distinct_mutants = set()
        for mutation in self.mutations:
            mutant_codes = molecule.mutate_code(mutation)
            distinct_mutants = distinct_mutants.union(mutant_codes)
        return distinct_mutants

    def molecule_to_e(self):
        mutations = self.mutations.copy()

        while True:
            try:
                random.shuffle(mutations)
                molecule = Molecule(self.molecule.code)
                return molecule.to_e(mutations)
            except ValueError as e:
                # Rotate until we get the right one
                print(mutations[0], e)
                rotated_mutation = mutations.pop(0)
                mutations.append(rotated_mutation)

    def mutate(self, rna, molecule):
        mutants = []
        start_at = rna.deviates_at(molecule)
        mutations = self.mutate_at(rna.code, start_at)
        for mutation in mutations:
            mutant = rna.clone()
            mutant.mutate(mutation)
            mutants.append(mutant)
        return mutants

    def mutate_at(self, code, index):
        distinct_mutants = set()
        for transform in self.mutations:
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

    def register_rna(self, rna):
        if rna.head in self.rna_registry:
            self.rna_registry[rna.head].append(rna.tail)
        else:
            self.rna_registry[rna.head] = [rna.tail]

    def rna_is_registered(self, rna):
        tails = self.rna_registry.get(rna.head, [])
        return rna.tail in tails

    def synthesize_molecule(self, molecule):
        cloned = []
        discards = 0
        queue = PriorityQueue()
        quickest = None
        leader = None

        rna = ReindeerNucleicAcid('e', molecule)
        self.register_rna(rna)
        queue.put(rna)
        leader = rna

        while not queue.empty():
            rna = queue.get()
            mutants = rna.mutate(self)

            for mutant in mutants:
                info((queue.qsize(), discards, len(cloned), rna, leader), 1000)

                if mutant.is_complete():
                    cloned.append(mutant)
                    if not quickest or mutant.steps < quickest.steps:
                        quickest = mutant
                elif mutant.is_too_long():
                    discards += 1
                elif len(mutant.tail) > len(self.longest_mutation):
                    discards += 1
                else:
                    if not self.rna_is_registered(mutant):
                        self.register_rna(mutant)
                        queue.put(mutant)

                    if mutant.progress > leader.progress:
                        leader = mutant

        info(f"quickest: {quickest.steps} ({queue.qsize()}, {len(cloned)})")
        return quickest.steps


@total_ordering
class Molecule:
    def __init__(self, code):
        self.mutations = [code.strip()]

    def __eq__(self, other):
        return self.priority == other.priority

    def __lt__(self, other):
        return self.priority < other.priority

    @property
    def code(self):
        return self.mutations[-1]

    @property
    def steps(self):
        return len(self.mutations) - 1

    @property
    def priority(self):
        # https://stackoverflow.com/a/56782135/1093087
        length_asc = self.length
        steps_asc = self.steps
        fixed_asc = f'aaa{self.code}' if self.code.startswith('O') else self.code
        return (length_asc, steps_asc, fixed_asc)

    @property
    def length(self):
        return len(self.code)

    def to_e(self, mutations):
        while self.code != 'e':
            before = self.code

            for reaction in mutations:
                reactant, product = reaction
                while product in self.code:
                    code = self.code.replace(product, reactant, 1)
                    self.evolve(code)

            after = self.code
            if len(before) == len(after):
                raise ValueError(f"{self} stuck")

        return self.steps

    def mutate_code(self, mutation):
        mutant_codes = set()
        n = 0
        find, replace = mutation
        find_len = len(find)
        for n in range(self.length-find_len+1):
            seg_end = n+find_len
            segment = self.code[n:seg_end]
            info(f"{find} {segment}", 1000000)
            if segment == find:
                mutant_code = self.code[0:n] + replace + self.code[seg_end:]
                mutant_codes.add(mutant_code)
        return mutant_codes

    def clone(self):
        clone = Molecule(self.code)
        clone.mutations = self.mutations.copy()
        return clone

    def evolve(self, new_code):
        self.mutations.append(new_code)
        return self

    def __repr__(self):
        return f"<Molecule code={self.code} priority={self.priority} steps={self.steps}>"


@total_ordering
class ReindeerNucleicAcid:
    def __init__(self, code, target_molecule=None):
        self.mutations = [code.strip()]
        self.target = target_molecule

    def __eq__(self, other):
        return self.priority == other.priority

    def __lt__(self, other):
        return self.priority < other.priority

    @property
    def priority(self):
        # https://stackoverflow.com/a/56782135/1093087
        progress_desc = self.progress * -1
        head_ratio_desc = self.head_ratio * -1
        steps_asc = self.steps
        return (progress_desc, head_ratio_desc, steps_asc)

    @property
    def head_ratio(self):
        return len(self.head) / len(self.code) * 100

    @property
    def progress(self):
        return len(self.head) / len(self.target.code) * 100

    @property
    def code(self):
        return self.mutations[-1]

    @property
    def head(self):
        # Head of RNA code that matches head of target molecule code
        return self.code[:self.deviation_index]

    @property
    def tail(self):
        # Remaining code that does not match target molecule
        if not self.head:
            return self.code
        _, tail = self.code.split(self.head, 1)
        return tail

    @property
    def deviation_index(self):
        """
        Returns index at which code deviates.

        Where self = 'abc' and other = 'adef', size would be 1
        Where self = 'abc' and other = 'abee', size would be 3
        Where self = 'bca' and other = 'abc', size would be 0
        """
        for n, chr in enumerate(self.code):
            if chr != self.target.code[n]:
                return n
        return n + 1

    @property
    def steps(self):
        return len(self.mutations) - 1

    def mutate(self, reactor):
        mutants = []
        uniq_codes = set()

        # Mutates tail against reaction mutations
        for mutation in reactor.mutations:
            rna = Molecule(self.code)
            mutated_rna = rna.mutate_code(mutation)
            uniq_codes = uniq_codes.union(mutated_rna)

        for code in uniq_codes:
            mutant = self.clone()
            mutant.evolve(code)
            mutants.append(mutant)

        return mutants

    def mutate_tail(self, reactor):
        mutants = []
        uniq_mutant_tails = set()

        # Mutates tail against reaction mutations
        for mutation in reactor.mutations:
            fragment = Molecule(self.tail)
            mutated_tails = fragment.mutate_code(mutation)
            uniq_mutant_tails = uniq_mutant_tails.union(mutated_tails)

        for mutant_tail in uniq_mutant_tails:
            code = self.head + mutant_tail
            mutant = self.clone()
            mutant.evolve(code)
            mutants.append(mutant)

        return mutants

    def evolve(self, new_code):
        self.mutations.append(new_code)
        return self

    def clone(self):
        clone = ReindeerNucleicAcid(self.code, self.target)
        clone.mutations = self.mutations.copy()
        return clone

    def is_complete(self):
        return self.code == self.target.code

    def is_too_long(self):
        return len(self.code) > len(self.target.code)

    def __repr__(self):
        prog = self.progress
        pri = self.priority
        return f"<RNA progress={prog:.1f} priority={pri} steps={self.steps} {self.code}>"


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
        min_steps = reactor.molecule_to_e()
        assert min_steps == 207, min_steps
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
        min_steps = reactor.molecule_to_e()
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
