"""
Advent of Code 2021 - Day 12
https://adventofcode.com/2021/day/12
"""
from os.path import join as path_join
from functools import cached_property
from config import INPUT_DIR


DAY_NUM = 12
FNAME = 'day-{:02d}.txt'.format(DAY_NUM)
INPUT_FILE = path_join(INPUT_DIR, FNAME)


class Solution:
    def __init__(self, input_file):
        self.input_file = input_file

    #
    # Solutions
    #
    @property
    def first(self):
        paths = []
        complete_paths = []
        complete = False
        print(self.starters)

        for edge in self.starters:
            path = ['start']
            next = self.pop_edge_partner(edge, 'start')
            path.append(next)
            paths.append(path)

        while not complete:
            new_paths = []
            for path in paths:
                valid_paths = self.filter_valid_paths(path)
                new_paths += valid_paths

            complete = all([path[-1] == 'end' for path in new_paths])
            paths = new_paths
            print(paths)

        return len(paths)

    def pop_edge_partner(self, edge, node):
        print(edge, node)
        pair = edge.copy()
        pair.remove(node)
        return pair[0]

    def filter_valid_paths(self, path):
        new_paths = []
        last_cave = path[-1]
        penult_cave = path[-2]

        # No more routes if this path at end
        if last_cave == 'end':
            return [path]

        # Find connecting nodes
        for edge in self.edges:
            # Skip unconnected path
            if last_cave not in edge:
                continue

            next_cave = self.pop_edge_partner(edge, last_cave)

            # Skip small caves that have already been visits
            if next_cave.islower() and next_cave in path:
                continue

            # Create new path
            new_path = path.copy()
            new_path.append(next_cave)
            new_paths.append(new_path)

        return new_paths

    @property
    def second(self):
        pass

    #
    # Properties
    #
    @cached_property
    def input_lines(self):
        with open(self.input_file) as file:
            lines = file.readlines()
            return [line.strip() for line in lines]

    @cached_property
    def edges(self):
        pairs = []
        for line in self.input_lines:
            pair = line.split('-')
            pairs.append(pair)
        return pairs

    @cached_property
    def starters(self):
        starts = []
        for pair in self.edges:
            if 'start' in pair:
                starts.append(pair)
        return starts

    @cached_property
    def enders(self):
        ends = []
        for pair in self.edges:
            if 'end' in pair:
                ends.append(pair)
        return ends


    #
    # Methods
    #


#
# Main
#
solution = Solution(INPUT_FILE)
print("pt 1 solution: {}".format(solution.first))
print("pt 2 solution: {}".format(solution.second))
