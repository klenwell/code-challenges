"""
Advent of Code 2015 - Day 7
https://adventofcode.com/2015/day/7
"""
from os.path import join as path_join
from functools import cached_property
from common import INPUT_DIR


class Circuit:

    GATES = {
        'AND': '&',
        'OR': '|',
        'LSHIFT': '<<',
        'RSHIFT': '>>',
        'NOT': '~'
    }

    def __init__(self, booklet):
        self.booklet = booklet
        self.signals = {}

    @cached_property
    def instructions(self):
        return self.booklet.strip().split('\n')

    @property
    def wires(self):
        wires = {}
        for instruction in self.instructions:
            gate, wire = instruction.split(' -> ')
            wires[wire] = self.parse_gate(gate)
        return wires

    def parse_gate(self, gate):
        # return wire id as str or operation as tuple (op, v1, v2)
        if gate.isdigit():
            return gate
        elif 'AND' in gate:
            w1, w2 = gate.split(' AND ')
            return ('&', w1, w2)
        elif 'OR' in gate:
            w1, w2 = gate.split(' OR ')
            return ('|', w1, w2)
        elif 'LSHIFT' in gate:
            wire, shift = gate.split(' LSHIFT ')
            return ('<<', wire, shift)
        elif 'RSHIFT' in gate:
            wire, shift = gate.split(' RSHIFT ')
            return ('>>', wire, shift)
        elif gate.startswith('NOT'):
            # To get non-negative complement: https://stackoverflow.com/a/16255550/1093087
            # int(bin(~i % (1<<16)), 2)
            _, wire = gate.split('NOT ')
            return ('NOT', wire, '1')
        else:
            #raise ValueError(f"Gate not found: {gate}")
            wire = gate
            return ('*', wire, '1')

    def parse_gate_v1(self, gate):
        if gate.isdigit():
            return gate
        elif gate.startswith('NOT'):
            # To get non-negative complement: https://stackoverflow.com/a/16255550/1093087
            # int(bin(~i % (1<<16)), 2)
            _, wire = gate.split('NOT ')
            return f"int(bin(~ self.wires['{wire}'] % (1<<16)), 2)"
        elif 'AND' in gate:
            w1, w2 = gate.split(' AND ')
            return f"self.wires['{w1}'] & self.wires['{w2}']"
        elif 'OR' in gate:
            w1, w2 = gate.split(' OR ')
            return f"self.wires['{w1}'] | self.wires['{w2}']"
        elif 'LSHIFT' in gate:
            wire, shift = gate.split(' LSHIFT ')
            return f"self.wires['{wire}'] << {shift}"
        elif 'RSHIFT' in gate:
            wire, shift = gate.split(' RSHIFT ')
            return f"self.wires['{wire}'] >> {shift}"
        else:
            #raise ValueError(f"Gate not found: {gate}")
            return f"self.wires['{gate}']"

    def get_signal(self, wire):
        if wire in self.signals:
            return self.signals[wire]

        print('get_signal', wire)
        gate = self.wires[wire]

        if type(gate) is tuple:
            op, v1, v2 = gate
            a = v1 if v1.isdigit() else self.get_signal(v1)
            b = v2 if v2.isdigit() else self.get_signal(v2)

            if op == 'NOT':
                expr = f"int(bin(~ {a} % (1<<16)), 2)"
            else:
                expr = f"{a} {op} {b}"
            signal = eval(expr)
        else:
            signal = gate

        print('got_signal', wire, gate, signal)
        #breakpoint()
        self.signals[wire] = int(signal)
        return int(signal)


class DailyPuzzle:
    INPUT_FILE = path_join(INPUT_DIR, 'day-07.txt')

    TEST_INPUT = """\
123 -> x
456 -> y
x AND y -> d
x OR y -> e
x LSHIFT 2 -> f
y RSHIFT 2 -> g
NOT x -> h
NOT y -> i"""

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
        breakpoint()
        input = self.file_input
        circuit = Circuit(input)
        return circuit.get_signal('a')

    @property
    def second(self):
        pass

    #
    # Tests
    #
    @property
    def test1(self):
        wire_signals = [
            # wire, signal
            ('d', 72),
            ('e', 507),
            ('f', 492),
            ('g', 114),
            ('h', 65412),
            ('i', 65079),
            ('x', 123),
            ('y', 456),
        ]

        input = self.TEST_INPUT
        circuit = Circuit(input)

        for wire, expected_signal in wire_signals:
            signal = circuit.get_signal(wire)
            assert signal == expected_signal, (wire, signal, expected_signal)

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
