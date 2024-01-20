"""
Advent of Code 2023 - Day 20
https://adventofcode.com/2023/day/20
"""
from os.path import join as path_join
from functools import cached_property
from common import INPUT_DIR, info


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
            #print(mod, '>', dest_names)
            cables[mod] = tuple(dest_names)

        # Don't forget to wire up the button
        button = ButtonModule('button')
        cables[button] = tuple(['broadcaster'])

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

    @cached_property
    def flip_flop_modules(self):
        mods = []
        for mod in self.modules:
            if isinstance(mod, FlipFlopModule):
                mods.append(mod)
        return mods

    def mash_button(self, times):
        for _ in range(times):
            self.push_button()

    def push_button(self):
        pulse = 'low'
        button = self.module_name_map['button']
        broadcaster = self.module_name_map['broadcaster']
        self.relay_pulse_to_module(button, pulse, broadcaster)

    def relay_pulse_to_module(self, origin, pulse, destination):
        info(f"{origin.name} --{pulse}--> {destination.name}", 1000)
        pulse = origin.send_pulse(pulse)
        next_pulse = destination.receive_pulse_from_mod(pulse, origin)

        if next_pulse:
            mod_names = self.cables[destination]
            for name in mod_names:
                next_mod = self.module_name_map[name]
                self.relay_pulse_to_module(destination, next_pulse, next_mod)

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
        self.last_pulse_from = {}
        self.pulses_sent = {
            'low': 0,
            'high': 0
        }

    @property
    def name(self):
        return self.id[1:]

    def receive_pulse_from_mod(self, type, origin_mod):
        # Return type of pulse output
        raise NotImplementedError('Must be overriden')

    def send_pulse(self, type):
        self.pulses_sent[type] += 1
        return type

    def __repr__(self):
        on_off = 'ON' if self.state == 1 else 'off'
        return f"<{self.__class__.__name__} name={self.name} {on_off} {self.pulses_sent}>"


class FlipFlopModule(PulseModule):
    def receive_pulse_from_mod(self, type, origin_mod):
        # If a flip-flop module receives a high pulse, it is ignored and nothing happens.
        if type == 'high':
            return None

        # However, if a flip-flop module receives a low pulse, it flips between on and off.
        # If it was off, it turns on and sends a high pulse. If it was on, it turns off and
        # sends a low pulse.
        if self.state == 0:
            self.state = 1
            return 'high'
        else:
            self.state = 0
            return 'low'


class ConjunctionModule(PulseModule):
    @property
    def pulse_type(self):
        # Conjunction modules (prefix &) remember the type of the most recent pulse received
        # from each of their connected input modules; they initially default to remembering a
        # low pulse for each input. When a pulse is received, the conjunction module first updates
        # its memory for that input. Then, if it remembers high pulses for all inputs, it sends a
        # low pulse; otherwise, it sends a high pulse.
        memory_set = set(list(self.last_pulse_from.values()))
        if memory_set == set(['high']):
            return 'low'
        else:
            return 'high'

    def receive_pulse_from_mod(self, type, origin_mod):
        self.last_pulse_from[origin_mod] = type
        return self.pulse_type


class BroadcasterModule(PulseModule):
    @property
    def name(self):
        return 'broadcaster'

    def receive_pulse_from_mod(self, type, origin_mod):
        # There is a single broadcast module (named broadcaster). When it receives a pulse, it
        # sends the same pulse to all of its destination modules.
        return type


class ButtonModule(PulseModule):
    @property
    def name(self):
        return 'button'


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

        # After this sequence, the flip-flop modules all end up off, so pushing the button again
        # repeats the same sequence.
        network = PulseNetwork(input)
        network.push_button()
        for mod in network.flip_flop_modules:
            assert mod.state == 0, mod
        assert network.pulse_product == 32, network

        # In the first example... after pushing the button 1000 times, 8000 low pulses and
        # 4000 high pulses are sent. Multiplying these together gives 32000000.
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
