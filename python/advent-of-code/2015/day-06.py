"""
Advent of Code 2015 - Day 6
https://adventofcode.com/2015/day/6
"""
from os.path import join as path_join
from functools import cached_property
from common import INPUT_DIR


class DisplayGrid:
    def __init__(self, input):
        self.input = input
        self.lights = self.init_grid()

    @cached_property
    def instructions(self):
        instructions = []
        for line in self.input.strip().split('\n'):
            instruction = Instruction(line)
            instructions.append(instruction)
        return instructions

    def configure(self):
        for n, instruction in enumerate(self.instructions):
            for pt in instruction.pts:
                if instruction.turn_on:
                    self.lights[pt] = 1
                elif instruction.turn_off:
                    self.lights[pt] = 0
                elif instruction.toggle:
                    self.toggle(pt)
            print(n, instruction.line) if n % 30 == 0 else None
        return self.lights

    def reconfigure(self):
        for n, instruction in enumerate(self.instructions):
            for pt in instruction.pts:
                if instruction.turn_on:
                    self.lights[pt] += 1
                elif instruction.turn_off and self.lights[pt] >= 1:
                    self.lights[pt] -= 1
                elif instruction.toggle:
                    self.lights[pt] += 2
            print(n, instruction.line) if n % 30 == 0 else None

        brightness = sum([v for v in self.lights.values()])
        return brightness

    def init_grid(self):
        lights = {}
        for y in range(1000):
            for x in range(1000):
                pt = (x, y)
                lights[pt] = 0
        return lights

    def toggle(self, pt):
        if self.lights[pt] == 1:
            self.lights[pt] = 0
        else:
            self.lights[pt] = 1
        return self


class Instruction:
    def __init__(self, line):
        self.line = line

    @property
    def pts(self):
        pts = []
        (x1, y1) = self.start_pt
        (x2, y2) = self.end_pt

        ys = sorted([y1, y2])
        xs = sorted([x1, x2])

        for x in range(xs[0], xs[1]+1):
            for y in range(ys[0], ys[1]+1):
                pts.append((x, y))

        return pts

    @property
    def start_pt(self):
        pre, _ = self.line.split(' through ')
        _, post = pre.rsplit(' ', 1)
        x, y = post.split(',')
        return (int(x), int(y))

    @property
    def end_pt(self):
        _, post = self.line.split(' through ', 1)
        x, y = post.split(',')
        return (int(x), int(y))

    @property
    def turn_off(self):
        return self.line.startswith('turn off')

    @property
    def turn_on(self):
        return self.line.startswith('turn on')

    @property
    def toggle(self):
        return self.line.startswith('toggle')


class DailyPuzzle:
    INPUT_FILE = path_join(INPUT_DIR, 'day-06.txt')

    TEST_INPUT = """\
"""

    def solve(self):
        print(f"test 1 solution: {self.test1}")
        #print(f"Part 1 Solution: {self.first}")
        print(f"test 2 solution: {self.test2}")
        print(f"Part 2 Solution: {self.second}")

    #
    # Solutions
    #
    @property
    def first(self):
        input = self.file_input
        grid = DisplayGrid(input)
        lights = grid.configure()
        lit_count = len([pt for pt, lit in grid.lights.items() if lit == 1])
        return lit_count

    @property
    def second(self):
        input = self.file_input
        grid = DisplayGrid(input)
        brightness = grid.reconfigure()
        return brightness

    #
    # Tests
    #
    @property
    def test1(self):
        test_cases = [
            # instruction, (on, off, toggle), num lights
            ('turn on 0,0 through 999,999', (1, 0, 0), 1000*1000),
            ('toggle 0,0 through 999,0', (0, 0, 1), 1000),
            ('turn off 499,499 through 500,500', (0, 1, 0), 4)
        ]

        for input, actions, lights in test_cases:
            instruction = Instruction(input)
            on, off, toggle = actions
            assert instruction.turn_on == bool(on), (input, on)
            assert instruction.turn_off == bool(off), (input, off)
            assert instruction.toggle == bool(toggle), (input, toggle)
            assert len(instruction.pts) == lights, (input, len(instruction.pts), lights)

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
problem = DailyPuzzle()
problem.solve()
