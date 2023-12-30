"""
Advent of Code 2023 - Day 15
https://adventofcode.com/2023/day/15
"""
from os.path import join as path_join
from functools import cached_property
from common import INPUT_DIR

from dataclasses import dataclass


class HolidayHash:
    def __init__(self, input):
        self.input = input.strip()

    @cached_property
    def sum(self):
        sum = 0
        for step in self.steps:
            hash = self.hash_value(step)
            sum += hash
        return sum

    @cached_property
    def focusing_power(self):
        boxes = {}
        for n in range(256):
            boxes[n] = Box(n)

        for step in self.steps:
            remove_lens = '-' in step
            if remove_lens:
                label = step[0:-1]
                n = self.hash_value(label)
                box = boxes[n]
                box.remove(label)
            else:
                label, focal_len = step.split('=')
                lens = Lens(label, int(focal_len))
                n = self.hash_value(label)
                box = boxes[n]
                box.upsert(lens)
            print(step, box)

        power = 0
        for box in boxes.values():
            power += box.focusing_power
        return power

    @cached_property
    def steps(self):
        return self.input.split(',')

    def hash_value(self, input):
        hash = 0
        for c in list(input):
            hash += ord(c)
            hash *= 17
            hash = hash % 256
        return hash


class Box:
    def __init__(self, num):
        self.number = num
        self.lenses = []
        self.labels = []

    @property
    def focusing_power(self):
        total_power = 0
        coeff = self.number+1
        for slot, lens in enumerate(self.lenses):
            power = (self.number+1) * (slot+1) * lens.focal_len
            total_power += power
        return total_power

    def remove(self, label):
        if label in self.labels:
            index = self.labels.index(label)
            self.labels.pop(index)
            self.lenses.pop(index)
        return self

    def upsert(self, lens):
        if lens.label in self.labels:
            index = self.labels.index(lens.label)
            self.lenses[index] = lens
        else:
            self.lenses.append(lens)
            self.labels.append(lens.label)

    def __repr__(self):
        return f"<Box #{self.number} lenses={self.lenses}>"


@dataclass
class Lens():
    label: str
    focal_len: int


class AdventPuzzle:
    INPUT_FILE = path_join(INPUT_DIR, 'day-15.txt')

    TEST_INPUT = """rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"""

    #
    # Solutions
    #
    @property
    def first(self):
        input = self.file_input
        hash = HolidayHash(input)
        return hash.sum

    @property
    def second(self):
        input = self.file_input
        hash = HolidayHash(input)
        return hash.focusing_power

    #
    # Tests
    #
    @property
    def test1(self):
        value = "HASH"
        hash = HolidayHash('')
        value = hash.hash_value(value)
        assert value == 52, value

        input = self.TEST_INPUT
        hash = HolidayHash(input)
        assert hash.sum == 1320, hash.sum
        return 'passed'

    @property
    def test2(self):
        input = self.TEST_INPUT
        hash = HolidayHash(input)
        assert hash.focusing_power == 145, hash.focusing_power
        return 'passed'

    #
    # Etc...
    #
    @cached_property
    def file_input(self):
        with open(self.INPUT_FILE) as file:
            return file.read().strip()

    def solve(self):
        print(f"test 1 solution: {self.test1}")
        print(f"Part 1 Solution: {self.first}")
        print(f"test 2 solution: {self.test2}")
        print(f"Part 2 Solution: {self.second}")


#
# Main
#
puzzle = AdventPuzzle()
puzzle.solve()
