"""
Advent of Code 2015 - Day 23
https://adventofcode.com/2015/day/23
"""
from os.path import join as path_join
from functools import cached_property
from common import INPUT_DIR


class Computer:
    def __init__(self):
        self.registers = {
            'a': 0,
            'b': 0
        }
        self.index = 0

    def run(self, program):
        instructions = program.split("\n")

        while self.index < len(instructions):
            method, args = self.parse(instructions[self.index])
            method(*args)
            print(self)

        return self

    def parse(self, instruction):
        print(instruction)
        method_attr, args = instruction.split(' ', 1)
        method = getattr(self, method_attr)
        return method, args.split(' ')

    def inc(self, register):
        self.registers[register] += 1
        self.index += 1
        return self

    def jio(self, register, offset):
        register = register[0]
        is_odd = self.registers[register] % 2 == 1

        if not is_odd:
            self.index += 1
        else:
            self.index += int(offset)

        return self

    def __repr__(self):
        return f"<Computer registers={self.registers} index={self.index}>"


class AdventPuzzle:
    INPUT_FILE = path_join(INPUT_DIR, 'day-23.txt')

    TEST_INPUT = """\
inc a
jio a, +2
tpl a
inc a"""

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
        pc = Computer()
        pc.run(input)
        return pc.registers['b']

    @property
    def second(self):
        pass

    #
    # Tests
    #
    @property
    def test1(self):
        input = self.TEST_INPUT
        pc = Computer()
        pc.run(input)
        assert pc.registers['a'] == 2
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
