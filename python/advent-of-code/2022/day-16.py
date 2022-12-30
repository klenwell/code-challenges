"""
Advent of Code 2022 - Day 16
https://adventofcode.com/2022/day/16
"""
from os.path import join as path_join
from functools import cached_property
from config import INPUT_DIR

import re


INPUT_FILE = path_join(INPUT_DIR, 'day-16.txt')

TEST_INPUT = """\
Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II"""


def extract_numbers(str):
    return [int(d) for d in re.findall(r'-?\d+', str)]


class PipeNetwork:
    @staticmethod
    def from_valve_scans(scans):
        valves = [Valve(scan) for scan in scans]
        return PipeNetwork(valves)

    def __init__(self, valves, steps=None, valve_logs=None):
        self.valves = valves
        self.steps = steps.copy() if steps else ['AA']
        self.valve_logs = valve_logs.copy() if valve_logs else []

    def maximize_release(self, minutes):
        queue = [self]
        completed = []
        pruned = 0
        minute = 0

        while queue:
            network = queue.pop(0)

            # Branch
            for option in network.options:
                clone = network.clone()
                clone.act(option)

                if clone.minute >= minutes:
                    completed.append(clone)
                else:
                    queue.append(clone)

            # Prune
            if network.minute > minute:
                minute = network.minute
                before = len(queue)

                queue = network.prune(queue)

                pruned = len(queue) - before
                print(minute, len(queue), pruned, network)

        networks = sorted(completed, key=lambda n: n.flow)
        return networks[-1]

    def prune(self, clones):
        return clones

    def clone(self):
        return PipeNetwork(self.valves, self.steps, self.valve_logs)

    def act(self, action):
        open_valves = self.valve_logs[-1] if self.valve_logs else ()

        if action == 'OPEN':
            open_valves += (self.current_valve,)
            step = self.current_valve
        else:
            step = action

        self.valve_logs.append(open_valves)
        self.steps.append(step)
        return step

    @property
    def options(self):
        options = []
        valve = self.valves_by_label[self.current_valve]

        if valve.label not in self.open_valves:
            options.append('OPEN')

        for label in valve.neighbors:
            options.append(label)

        return options

    @property
    def current_valve(self):
        return self.steps[-1]

    @property
    def open_valves(self):
        # Flatten List: https://stackoverflow.com/a/12356856/1093087
        return set([label for labels in self.valve_logs for label in labels])

    @cached_property
    def valves_by_label(self):
        index = {}
        for valve in self.valves:
            index[valve.label] = valve
        return index

    @property
    def minute(self):
        return len(self.steps)

    @property
    def release(self):
        flow = 0
        for labels in self.valve_logs:
            for label in labels:
                flow += self.valves_by_label[label].flow
        return flow

    def __repr__(self):
        return f"<Network minute={self.minute} release={self.release}>"


class Valve:
    def __init__(self, scan):
        flow_rate, tunnels = scan.split(';')
        self.label = self.extract_label(flow_rate)
        self.flow = extract_numbers(flow_rate)[0]
        self.neighbors = self.extract_neighbors(tunnels)

    def extract_label(self, input):
        label, _ = input.split(' has flow')
        _, label = label.split(' ')
        return label

    def extract_neighbors(self, input):
        _, valves = input.split('valve')
        valves = valves[2:] if valves.startswith('s') else valves[1:]
        return [label.strip() for label in valves.split(',')]

    def __repr__(self):
        return f"<Valve lable={self.label} flow={self.flow} neighbors={self.neighbors}>"



class Solution:
    def __init__(self, input_file):
        self.input_file = input_file

    #
    # Solutions
    #
    @property
    def test1(self):
        scans = self.test_input_lines
        minutes = 30

        # Test Valve
        valve = Valve(scans[0])
        assert valve.label == 'AA', valve

        # Test Network
        network = PipeNetwork.from_valve_scans(scans)
        network = network.maximize_release(minutes)
        print(network)


    @property
    def first(self):
        return self.input_lines

    @property
    def test2(self):
        pass

    @property
    def second(self):
        pass

    #
    # Properties
    #
    @cached_property
    def file_input(self):
        with open(self.input_file) as file:
            return file.read().strip()

    @cached_property
    def input_lines(self):
        return [line.strip() for line in self.file_input.split("\n")]

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
print("pt 1 solution: {}".format(solution.first))
print("test 2 solution: {}".format(solution.test2))
print("pt 2 solution: {}".format(solution.second))
