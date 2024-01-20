"""
Advent of Code 2023 - Day 20
https://adventofcode.com/2023/day/20
"""
from os.path import join as path_join
from functools import cached_property
from common import INPUT_DIR


class PulseNetwork:
    def __init__(self, input):
        self.input = input.strip()

    @property
    def low_pulses(self):
        return sum([m.pulses_sent['low'] for m in self.modules])

    @property
    def high_pulses(self):
        return sum([m.pulses_sent['high'] for m in self.modules])

    @property
    def pulse_product(self):
        return self.low_pulses * self.high_pulses

    @cached_property
    def lines(self):
        return [line.strip() for line in self.input.split('\n')]

    @cached_property
    def cables(self):
        cables = {}
        for line in self.lines:
            mod_id, dest_names = line.split(' -> ')
            mod = PulseModule.create(mod_id)
            dest_names = [name.strip() for name in dest_names.split(',')]
            cables[mod] = tuple(dest_names)
        return cables

    @cached_property
    def module_name_map(self):
        map = {}
        for mod in self.modules:
            map[mod.name] = mod
        return map

    @cached_property
    def modules(self):
        return list(self.cables.keys())

    def mash_button(self, times):
        for _ in range(times):
            self.push_button()

    def push_button(self):
        pulse = 'low'
        self.relay_pulse_to_module(pulse, 'broadcaster')

    def relay_pulse_to_module(self, pulse, name):
        print(f"{pulse} to {name}")
        module = self.module_name_map['broadcaster']
        pulse = module.receive_pulse(pulse)

        if pulse:
            destinations = self.cables[module]
            for name in destinations:
                destination = self.module_name_map[name]
                self.relay_pulse_to_module(pulse, destination)

    def __repr__(self):
        return f"<Network pulse=({self.low_pulses}, {self.high_pulses})>"


class PulseModule:
    TYPES = {
        '%': 'flip-flop',
        '&': 'conjunction',
        'b': 'broadcaster'
    }

    @staticmethod
    def create(id):
        mod_type = PulseModule.TYPES.get(id[0])
        if mod_type == 'flip-flop':
            return FlipFlopModule(id)
        elif mod_type == 'conjunction':
            return ConjunctionModule(id)
        elif mod_type == 'broadcaster':
            return BroadcasterModule(id)
        else:
            raise Exception(f"Invalid module id: {id}")

    def __init__(self, id):
        self.id = id
        self.state = 0
        self.pulses_sent = {
            'low': 0,
            'high': 0
        }

    @property
    def name(self):
        return self.id[1:]

    def receive_pulse(self, type):
        pass

    def send_pulse(self, type):
        self.pulses_sent[type] += 1
        return type


class FlipFlopModule(PulseModule): pass


class ConjunctionModule(PulseModule): pass


class BroadcasterModule(PulseModule):
    @property
    def name(self):
        return 'broadcaster'


class AdventPuzzle:
    INPUT_FILE = path_join(INPUT_DIR, 'day-20.txt')

    TEST_INPUT = """\
broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a"""

    INTERESTING_TEST_INPUT = """\
broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output"""

    #
    # Solutions
    #
    @property
    def first(self):
        input = self.file_input
        return input

    @property
    def second(self):
        pass

    #
    # Tests
    #
    @property
    def test1(self):
        input = self.TEST_INPUT
        network = PulseNetwork(input)
        network.mash_button(1000)
        assert network.low_pulses == 8000, network
        assert network.high_pulses == 4000, network
        assert network.pulse_product == 32000000, network.pulse_product
        return 'passed'

    @property
    def test2(self):
        input = self.TEST_INPUT
        print(input)
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
