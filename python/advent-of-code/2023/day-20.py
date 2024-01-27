"""
Advent of Code 2023 - Day 20
https://adventofcode.com/2023/day/20
"""
from os.path import join as path_join
from functools import cached_property
from common import INPUT_DIR, info
import warnings

from models.day_20.pulse_module import PulseModule, FlipFlopModule, ButtonModule, TerminalModule


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

    def degrees_from(self, origin):
        tiers = []
        stack = [(origin, 0)]

        tiers.append((origin,))

        while stack:
            mod, degree = stack.pop()
            inputs = self.input_map[mod]
            print(mod, inputs, len(stack))

            if degree > 1:
                breakpoint()

            for input in inputs:
                stack.append((input, degree+1))

            if len(tiers) < degree + 2:
                tiers.append(tuple(inputs))
            else:
                existing_tier = tiers[degree+1]
                tiers[degree+1] = existing_tier + tuple(inputs)


        return tiers

    def relay_pulse_to_module(self, origin, pulse, destination):
        """Since this is recursive, this will not work. Recursion is stack-based so this ends
        up transmitting pulses in the wrong order (i.e. depth-first).
        """
        if self.debug:
            print(f"{origin.name} --{pulse}--> {destination.name}")

        info(f"{origin.name} --{pulse}--> {destination.name}", 1000)
        pulse = origin.send_pulse(pulse)
        next_pulse = destination.receive_pulse_from_mod(pulse, origin)

        if next_pulse:
            mod_names = self.cables[destination]
            for name in mod_names:
                next_mod = self.module_name_map.get(name)
                self.relay_pulse_to_module(destination, next_pulse, next_mod)

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

    @cached_property
    def rx_module(self):
        return self.network.module_name_map.get('rx')

    def turn_on(self):
        pushes = 0
        pulsed_mods = 0

        while self.is_off:
            self.network.push_button()
            pushes += 1
            info(f"{pushes} - {self.rx_module.pulses_received} {self.network}", 1000)

            # ons = [self.mod_on('dh'), self.mod_on('mk'), self.mod_on('vf'), self.mod_on('rn')]
            # on_sum = sum(ons)
            # if on_sum > 0:
            #     print(on_sum)
            #     breakpoint()

            last_count = pulsed_mods
            pulsed_mods = len(self.network.pulsed_mods.keys())
            if pulsed_mods > last_count:
                breakpoint()

            if self.completes_cycle():
                breakpoint()

        return pushes

    def completes_cycle(self):
        for mod in self.network.modules:
            if mod.name == 'button':
                continue
            if mod.state != mod.initial_state:
                return False
        return True

    def mod_on(self, mod):
        return self.network.module_name_map.get(mod).on


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
        presses = 0
        input = self.file_input
        machine = PulseMachine(input)
        presses = machine.turn_on()
        return presses

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
        #breakpoint()

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
        presses = 0
        input = self.file_input
        network = PulseNetwork(input)

        rx = network.module_name_map['rx']
        rx_inputs = network.input_map[rx]
        jz = rx_inputs[0]

        upstream_pulses = {}
        for upstream_mod in jz.last_pulse_from.keys():
            upstream_pulses[upstream_mod] = []

        for n in range(100000):
            network.push_button()
            for upstream_mod, high_pulses in upstream_pulses.items():
                if jz.last_pulse_from[upstream_mod] == 'high':
                    breakpoint()
                if upstream_mod.pulses_sent['high'] > len(high_pulses):
                    high_pulses.append(n)
            three_samples = [len(high_pulses) > 3 for high_pulses in upstream_pulses.values()]
            if all(three_samples):
                break

        print(upstream_pulses)
        breakpoint()

        cycled = False

        while not cycled:
            machine.network.push_button()
            presses += 1
            cycled = machine.completes_cycle()
            print(presses, cycled, machine.network)

        pulse_product = machine.network.pulse_product * (1000 / presses) * (1000 / presses)
        assert presses == 4, presses
        assert pulse_product == 11687500, pulse_product
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
