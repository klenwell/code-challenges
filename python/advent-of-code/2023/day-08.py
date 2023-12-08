"""
Advent of Code 2023 - Day 8
https://adventofcode.com/2023/day/8
"""
from os.path import join as path_join
from functools import cached_property
from common import INPUT_DIR


class DesertMap:
    def __init__(self, input):
        self.input = input.strip()

    @cached_property
    def instructions(self):
        code, _ = self.input.split('\n\n')
        return list(code.strip())

    @cached_property
    def nodes(self):
        nodes = {}
        _, block = self.input.split('\n\n')
        lines = block.strip().split('\n')
        for line in lines:
            id, left, right = self.parse_node(line)
            nodes[id] = (left, right)
        return nodes

    def walk_to_zzz(self):
        steps = 0
        node_id = 'AAA'

        while node_id != 'ZZZ':
            index = steps % len(self.instructions)
            direction = self.instructions[index]
            left, right = self.nodes[node_id]
            node_id = left if direction == 'L' else right
            steps += 1

        return steps

    def parse_node(self, line):
        id, opts = line.split(' = ')
        opts = opts.strip()[1:-1]
        left, right = opts.split(', ')
        return id.strip(), left.strip(), right.strip()


class GhostMap(DesertMap):
    @property
    def nodes_ending_in_a(self):
        node_ids = []
        for node_id in self.nodes.keys():
            if node_id[-1] == 'A':
                node_ids.append(node_id)
        return node_ids

    def walk_to_xxz(self):
        steps = 0
        node_ids = self.nodes_ending_in_a
        all_on_xxz = False

        while not all_on_xxz:
            index = steps % len(self.instructions)
            new_node_ids = []
            for node_id in node_ids:
                direction = self.instructions[index]
                left, right = self.nodes[node_id]
                new_node_id = left if direction == 'L' else right
                new_node_ids.append(new_node_id)
            steps += 1
            node_ids = new_node_ids
            all_on_xxz = all([n[-1] == 'Z' for n in node_ids])
            print(steps, all_on_xxz, node_ids)

        return steps


class AdventPuzzle:
    INPUT_FILE = path_join(INPUT_DIR, 'day-08.txt')

    TEST_INPUT = """\
LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)"""

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
        map = DesertMap(input)
        steps = map.walk_to_zzz()
        return steps

    @property
    def second(self):
        # Suspect this requires LCM. See:
        # https://github.com/klenwell/code-challenges/blob/main/python/advent-of-code/2022/day-11.py
        # https://docs.python.org/3/library/math.html#math.lcm
        input = self.file_input
        map = GhostMap(input)
        print(map.nodes_ending_in_a)
        steps = map.walk_to_xxz()
        return steps

    #
    # Tests
    #
    @property
    def test1(self):
        input = self.TEST_INPUT
        map = DesertMap(input)
        print(map.nodes)
        steps = map.walk_to_zzz()

        assert steps == 6, steps
        return 'passed'

    @property
    def test2(self):
        input = """\
LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)"""

        map = GhostMap(input)
        print(map.nodes_ending_in_a)
        steps = map.walk_to_xxz()
        assert steps == 6, steps
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
