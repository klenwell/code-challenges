"""
Advent of Code 2015 - Day 16
https://adventofcode.com/2015/day/16
"""
from os.path import join as path_join
from functools import cached_property
from common import INPUT_DIR
import json


class AuntDetector:
    def __init__(self, aunt_memories, ticker_tape):
        self.aunt_memories = aunt_memories.strip()
        self.ticker_tape = ticker_tape.strip()

    @cached_property
    def aunts(self):
        aunts = []
        for memory in self.aunt_memories.split('\n'):
            aunt = Aunt(memory)
            aunts.append(aunt)
        return aunts

    @cached_property
    def compounds(self):
        compounds = {}
        for key_val in self.ticker_tape.split('\n'):
            key, val = key_val.split(': ')
            compounds[key.strip()] = int(val.strip())
        return compounds

    def detect_sue(self):
        matches = []

        for aunt in self.aunts:
            match = True
            for key, val in aunt.attrs.items():
                if val != self.compounds[key]:
                    match = False
                    break
            if match:
                matches.append(aunt)

        if len(matches) != 1:
            print(len(matches))
            breakpoint()
        else:
            return matches[0].number


class Aunt:
    def __init__(self, memory):
        self.memory = memory

    @cached_property
    def number(self):
        id, attrs = self.memory.split(': ', 1)
        name, number = id.split(' ')
        return int(number)

    @cached_property
    def attrs(self):
        attrs = {}
        id, attr_csv = self.memory.split(': ', 1)
        for attr in attr_csv.split(', '):
            key, val = attr.split(': ')
            attrs[key.strip()] = int(val.strip())
        return attrs

    def __repr__(self):
        return f"<Aunt number={self.number} attrs={self.attrs}>"


class AdventPuzzle:
    INPUT_FILE = path_join(INPUT_DIR, 'day-16.txt')

    TEST_INPUT = """\
children: 3
cats: 7
samoyeds: 2
pomeranians: 3
akitas: 0
vizslas: 0
goldfish: 5
trees: 3
cars: 2
perfumes: 1"""

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
        ticker_tape = self.TEST_INPUT
        aunt_list = self.file_input
        detector = AuntDetector(aunt_list, ticker_tape)

        number = detector.detect_sue()
        return number

    @property
    def second(self):
        pass

    #
    # Tests
    #
    @property
    def test1(self):
        ticker_tape = self.TEST_INPUT
        aunt_list = self.file_input

        detector = AuntDetector(aunt_list, ticker_tape)
        assert len(detector.aunts) == 500, len(detector.aunts)
        assert detector.compounds['children'] == 3, detector.compounds

        aunt = detector.aunts[0]
        assert aunt.number == 1, aunt
        assert aunt.attrs == dict(goldfish=9, cars=0, samoyeds=9), aunt

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
