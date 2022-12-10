"""
Advent of Code 2022 - Day 10
https://adventofcode.com/2022/day/10
"""
from os.path import join as path_join
from functools import cached_property
from config import INPUT_DIR


INPUT_FILE = path_join(INPUT_DIR, 'day-10.txt')

TEST_INPUT = """\
addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop"""


class ElfCpu:
    def __init__(self, program):
        self.instructions = program.split("\n")
        self.x = 1
        self.tape = []

    @property
    def cycle(self):
        return len(self.tape)

    def signal_strength(self, cycle):
        return cycle * self.tape[cycle-1]

    def execute(self):
        for instruction in self.instructions:
            self.run(instruction)

    def run(self, instruction):
        if instruction.startswith('noop'):
            self.noop()
        else:
            self.addx(instruction)

    def noop(self):
        self.tape.append(self.x)

    def addx(self, command):
        _, val = command.split(' ')
        self.tape.append(self.x)
        self.tape.append(self.x)
        self.x += int(val)

    @property
    def crt(self):
        crt = [' '] * 240
        for n, x in enumerate(self.tape):
            crt_x = n % 40
            sprite = [x-1, x, x+1]
            crt[n] = '#' if crt_x in sprite else '.'
        return crt

    def render_image(self):
        for n in range(6):
            start_at = n * 40
            end_at = start_at + 40
            line = ''.join(self.crt[start_at:end_at])
            print(line)


class Solution:
    def __init__(self, input_file):
        self.input_file = input_file

    #
    # Solutions
    #
    @property
    def test1(self):
        small_program = """\
noop
addx 3
addx -5"""
        cpu = ElfCpu(small_program)
        cpu.execute()
        assert(cpu.x == -1)

        larger_program = TEST_INPUT
        cpu = ElfCpu(larger_program)
        cpu.execute()
        cycles = [20, 60, 100, 140, 180, 220]
        signals = [cpu.signal_strength(c) for c in cycles]
        return sum(signals)

    @property
    def first(self):
        program = self.input
        cpu = ElfCpu(program)
        cpu.execute()
        cycles = [20, 60, 100, 140, 180, 220]
        signals = [cpu.signal_strength(c) for c in cycles]
        return sum(signals)

    @property
    def test2(self):
        larger_program = TEST_INPUT
        cpu = ElfCpu(larger_program)
        cpu.execute()
        cpu.render_image()
        return '(see image above)'

    @property
    def second(self):
        program = self.input
        cpu = ElfCpu(program)
        cpu.execute()
        cpu.render_image()
        return '(see image above)'

    #
    # Properties
    #
    @cached_property
    def input(self):
        with open(self.input_file) as file:
            return file.read().strip()

    @cached_property
    def input_lines(self):
        with open(self.input_file) as file:
            lines = file.readlines()
            return [line.strip() for line in lines]

    @cached_property
    def test_input_lines(self):
        return [line.strip() for line in TEST_INPUT.split("\n")]

    #
    # Methods
    #


#
# Main
#
solution = Solution(INPUT_FILE)
print("test 1 solution: {}".format(solution.test1))
print("test 2 solution: {}".format(solution.test2))
print("pt 1 solution: {}".format(solution.first))
print("pt 2 solution: {}".format(solution.second))
