"""
Advent of Code 2023 - Day 20
https://adventofcode.com/2023/day/20
"""
from os.path import join as path_join
from functools import cached_property
from common import INPUT_DIR
import warnings
import math

from models.day_20.pulse_module import (PulseModule, FlipFlopModule, ConjunctionModule,
                                        ButtonModule, TerminalModule)


class PulseNetwork:
    def __init__(self, input, debug=False):
        self.input = input.strip()
        self.debug = debug
        self.queue = []
        self.wire_up_modules()

    def wire_up_modules(self):
        for mod, input_mods in self.input_map.items():
            mod.wire_up_inputs(input_mods)
        return self

    @cached_property
    def input_map(self):
        map = {}
        for input, output_names in self.cables.items():
            for name in output_names:
                output = self.module_name_map.get(name)

                # Untyped modules "for testing purposes"
                if not output:
                    warnings.warn(f"terminal module: {name}")
                    continue

                if output in map:
                    map[output].append(input)
                else:
                    map[output] = [input]
        return map

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
        mods = list(self.cables.keys())
        mod_names = [m.name for m in mods]

        for cable_mod_names in self.cables.values():
            for name in cable_mod_names:
                if name not in mod_names:
                    mod = TerminalModule(name)
                    mods.append(mod)
                    mod_names.append(name)

        return mods

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
        self.relay_pulse(button, pulse, broadcaster)
        while self.queue:
            pulse = self.queue.pop(0)
            self.transmit_pulse(pulse)

    def relay_pulse(self, origin, pulse_type, destination):
        pulse = (origin, pulse_type, destination)
        self.queue.append(pulse)
        return self

    def transmit_pulse(self, pulse):
        origin, pulse_type, destination = pulse

        if self.debug:
            print(f"{origin.name} --{pulse_type}--> {destination.name}")

        pulse_type = origin.send_pulse(pulse_type)
        next_pulse = destination.receive_pulse_from_mod(pulse_type, origin)

        if next_pulse:
            mod_names = self.cables[destination]
            for name in mod_names:
                next_mod = self.module_name_map.get(name)
                self.relay_pulse(destination, next_pulse, next_mod)

    def __repr__(self):
        return f"<Network pulse=({self.low_pulses}, {self.high_pulses})>"


class PulseMachine:
    def __init__(self, input):
        self.network = PulseNetwork(input)
        self.off = True
        self.button_pushes = 0

    @property
    def is_off(self):
        return self.rx_module.pulses_received['low'] == 0

    @property
    def rx_module(self):
        return self.network.module_name_map.get('rx')

    @property
    def rx_input_cycles(self):
        rx_inputs = self.network.input_map[self.rx_module]
        rx_input_mod = rx_inputs[0]

        input_pulses = {}

        for upstream_mod in rx_input_mod.last_pulse_from.keys():
            input_pulses[upstream_mod] = []

        # Find cycles to emit high pulse needed by rx_input to send low pulse to rx
        for n in range(100000):
            self.network.push_button()

            for upstream_mod, high_pulses in input_pulses.items():
                is_new_high_pulse = upstream_mod.pulses_sent['high'] > len(high_pulses)
                if is_new_high_pulse:
                    high_pulses.append(n)

            # Collect at least 2 samples
            have_samples = [len(ips) >= 2 for ips in input_pulses.values()]

            if all(have_samples):
                break

        return [ips[1]-ips[0] for ips in input_pulses.values()]

    @property
    def button_presses_to_turn_on(self):
        return math.lcm(*self.rx_input_cycles)


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
        network = PulseNetwork(input)
        network.mash_button(1000)
        return network.pulse_product

    @property
    def second(self):
        input = self.file_input
        machine = PulseMachine(input)
        return machine.button_presses_to_turn_on

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
            assert mod.on == 0, mod
        assert network.pulse_product == 32, network

        # In the first example... after pushing the button 1000 times, 8000 low pulses and
        # 4000 high pulses are sent. Multiplying these together gives 32000000.
        network = PulseNetwork(input)
        network.mash_button(1000)
        assert network.low_pulses == 8000, network
        assert network.high_pulses == 4000, network
        assert network.pulse_product == 32000000, network.pulse_product

        #
        # Test B
        #
        input = self.INTERESTING_TEST_INPUT
        network = PulseNetwork(input, True)
        network.push_button()

        # In the second example, after pushing the button 1000 times, 4250 low pulses and
        # 2750 high pulses are sent. Multiplying these together gives 11687500.
        network = PulseNetwork(input)
        network.mash_button(1000)
        assert network.low_pulses == 4250, network
        assert network.high_pulses == 2750, network
        assert network.pulse_product == 11687500, network.pulse_product
        return 'passed'

    @property
    def test2(self):
        input = self.file_input
        network = PulseNetwork(input)

        # Confirm there is only one rx input that is ConjunctionModule
        rx = network.module_name_map['rx']
        rx_inputs = network.input_map[rx]
        assert len(rx_inputs) == 1, rx_inputs
        assert isinstance(rx_inputs[0], ConjunctionModule), rx_inputs[0]
        assert rx_inputs[0].name == 'jz', rx_inputs[0]

        # jz is a ConjunctionModule that needs to receive high pulse from all its inputs in
        # order to send the low pulse to rx that we're looking for
        jz = rx_inputs[0]

        upstream_pulses = {}
        for upstream_mod in jz.last_pulse_from.keys():
            upstream_pulses[upstream_mod] = []

        for n in range(100000):
            network.push_button()
            for upstream_mod, high_pulses in upstream_pulses.items():
                if upstream_mod.pulses_sent['high'] > len(high_pulses):
                    high_pulses.append(n)
            have_samples = [len(high_pulses) >= 2 for high_pulses in upstream_pulses.values()]
            if all(have_samples):
                break

        cycles = [ups[-1] - ups[-2] for ups in upstream_pulses.values()]
        assert all([cycle > 0 for cycle in cycles])
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
