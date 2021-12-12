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
        complete = False

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

        return len(paths)

    @property
    def second(self):
        open_paths = []
        complete_paths = []
        complete = False

        for next_cave in self.route_map['start']:
            path = ['start']
            path.append(next_cave)
            open_paths.append(path)

        while not complete:
            new_paths = []
            for path in open_paths:
                valid_paths = self.filter_valid_paths_v2(path)

                for path in valid_paths:
                    if path[-1] == 'end':
                        complete_paths.append(path)
                    else:
                        new_paths.append(path)
                        if len(new_paths) % 50000 == 0:
                            breakpoint()

            open_paths = new_paths
            complete = len(open_paths) < 1
            print(len(open_paths), len(complete_paths))
            if len(complete_paths) > 240550:
                raise ValueError("Too many paths: {}".format(len(complete_paths)))

        return len(complete_paths)

    @cached_property
    def route_map(self):

        index = {}
        for edge in self.edges:
            c1, c2 = edge

            # Update c1 index
            c1_map = index.get(c1, set())
            if c2 != 'start':
                c1_map.add(c2)
                index[c1] = c1_map

            # Update c2 index
            c2_map = index.get(c2, set())
            if c1 != 'start':
                c2_map.add(c1)
                index[c2] = c2_map

        # 'end' is terminal
        index['end'] = set()
        return index

    def pop_edge_partner(self, edge, cave):
        pair = edge.copy()
        pair.remove(cave)
        return pair[0]

    def filter_valid_paths(self, path):
        new_paths = []
        last_cave = path[-1]

        # No more routes if this path at end
        if last_cave == 'end':
            return [path]

        # Find connecting nodes
        for next_cave in self.route_map[last_cave]:
            # Skip small caves that have already been visited
            if next_cave.islower() and next_cave in path:
                continue

            # Create new path
            new_path = path.copy()
            new_path.append(next_cave)
            new_paths.append(new_path)

        return new_paths

    def filter_valid_paths_v2(self, path):
        new_paths = []
        last_cave = path[-1]

        # No more routes if this path at end
        if last_cave == 'end':
            return [path]

        # Find connecting nodes
        for next_cave in self.route_map[last_cave]:
            # Skip if already visited one small cave twice
            # TODO: Fix this. If small cave, can visit if hasn't visit it yet or
            # hasn't visited a small cave twice
            if next_cave.islower() and next_cave in path:
                if self.visited_small_cave_twice(path):
                    continue

            # Create new path
            new_path = path.copy()
            new_path.append(next_cave)
            new_paths.append(new_path)

        return new_paths

    def visited_small_cave_twice(self, path):
        visited_caves = []

        for visited_cave in path:
            if not visited_cave.islower():
                continue

            if visited_cave in visited_caves:
                return True
            else:
                visited_caves.append(visited_cave)

        return False


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
