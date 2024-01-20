"""
Advent of Code 2023 - Day 20
https://adventofcode.com/2023/day/20
"""
from os.path import join as path_join
from functools import cached_property
from common import INPUT_DIR, info
import warnings


class PulseNetwork:
    def __init__(self, input, debug=False):
        self.input = input.strip()
        self.debug = debug
        self.queue = []
        self.reset_conjunction_modules()

    def reset_conjunction_modules(self):
        for mod, input_mods in self.input_map.items():
            if not isinstance(mod, ConjunctionModule):
                continue
            mod.reset_memory(input_mods)

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
    def terminal_mod_map(self):
        map = {}
        for mod_names in self.cables.values():
            for name in mod_names:
                if not self.module_name_map.get(name):
                    if name not in map:
                        mod = TerminalModule(name)
                        map[name] = mod
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

                if not next_mod:
                    next_mod = self.terminal_mod_map[name]

                self.relay_pulse(destination, next_pulse, next_mod)

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

                if not next_mod:
                    next_mod = self.terminal_mod_map[name]

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

    def reset_memory(self, input_mods):
        for input_mod in input_mods:
            self.last_pulse_from[input_mod] = 'low'
        return self

    def receive_pulse_from_mod(self, type, input_mod):
        self.last_pulse_from[input_mod] = type
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


class TerminalModule(PulseModule):
    @property
    def name(self):
        return self.id

    def receive_pulse_from_mod(self, type, origin_mod):
       return None


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
