"""
Advent of Code 2022 - Day 12
https://adventofcode.com/2022/day/12
"""
from os.path import join as path_join
from functools import cached_property
from config import INPUT_DIR

import heapq


INPUT_FILE = path_join(INPUT_DIR, 'day-12.txt')

TEST_INPUT = """\
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi"""


class ElevationMap:
    def __init__(self, input):
        self.input = input

    @cached_property
    def start_pt(self):
        for pt, letter in self.raw_grid.items():
            if letter == 'S':
                return pt

    @cached_property
    def end_pt(self):
        for pt, letter in self.raw_grid.items():
            if letter == 'E':
                return pt

    @cached_property
    def rows(self):
        rows = []
        for line in self.input.split('\n'):
            row = list(line)
            rows.append(row)
        return rows

    @cached_property
    def raw_grid(self):
        grid = {}
        for y, row in enumerate(self.rows):
            for x, letter in enumerate(row):
                pt = (x, y)
                grid[pt] = letter
        return grid

    @cached_property
    def grid(self):
        grid = {}
        for pt, letter in self.raw_grid.items():
            grid[pt] = self.elevation_to_int(letter)
        return grid

    @cached_property
    def grid_width(self):
        return len(self.rows[0])

    @cached_property
    def grid_height(self):
        return len(self.rows)

    @cached_property
    def shortest_path(self):
        return self.find_shortest_path(self.start_pt)

    def find_shortest_path(self, start_pt):
        path = []
        steps = self.dijkstra_improved(start_pt)

        path_found = steps.get(self.end_pt)
        if not path_found:
            return None

        step = self.end_pt
        while step:
            path.insert(0, step)
            step = steps[step]
        return path

    def elevation_to_int(self, letter):
        letter = 'a' if letter == 'S' else letter
        letter = 'z' if letter == 'E' else letter
        return ord(letter)

    def dijkstra(self, start_at):
        dists = {}
        steps = {}
        queue = []

        for pt in self.grid.keys():
            dists[pt] = 1000
            steps[pt] = None
            queue.append(pt)

        dists[start_at] = 0

        while len(queue) > 0:
            priority_q = [(dists[pt], pt) for pt in queue]
            pt = min(sorted(priority_q))[1]
            queue.remove(pt)

            if pt == self.end_pt:
                break

            for next_pt in self.neighbors(pt):
                if self.grid[next_pt] - self.grid[pt] > 1:
                    continue
                if next_pt not in queue:
                    continue

                dist = dists[pt] + 1
                if dist < dists[next_pt]:
                    dists[next_pt] = dist
                    steps[next_pt] = pt

        return steps

    def dijkstra_improved(self, start_at):
        open_paths = [(0, start_at)]
        steps = {start_at: None}
        costs = {start_at: 0}

        while open_paths:
            _, pt = heapq.heappop(open_paths)

            if pt == self.end_pt:
                break

            for next_pt in self.neighbors(pt):
                if self.grid[next_pt] - self.grid[pt] > 1:
                    continue
                if next_pt in costs:
                    continue

                cost = costs[pt] + 1
                costs[next_pt] = cost
                heapq.heappush(open_paths, (cost, next_pt))
                steps[next_pt] = pt

        return steps

    def neighbors(self, pt):
        x, y = pt
        if x > 0:
            yield (x - 1, y)
        if x < self.grid_width - 1:
            yield (x + 1, y)
        if y > 0:
            yield (x, y - 1)
        if y < self.grid_height - 1:
            yield (x, y + 1)


class Solution:
    def __init__(self, input_file):
        self.input_file = input_file

    #
    # Solutions
    #
    @property
    def test1(self):
        map = ElevationMap(TEST_INPUT)
        steps = len(map.shortest_path) - 1
        return steps

    @property
    def test2(self):
        path_steps = []
        map = ElevationMap(TEST_INPUT)
        low_points = [pt for pt, ht in map.grid.items() if ht == ord('a')]
        print(low_points)

        for start_pt in low_points:
            path = map.find_shortest_path(start_pt)
            if not path:
                continue

            steps = len(path) - 1
            print(start_pt, steps)
            path_steps.append(steps)

        return min(path_steps)

    @property
    def first(self):
        map = ElevationMap(self.file_input)
        steps = len(map.shortest_path) - 1
        return steps

    @property
    def second(self):
        path_steps = []
        map = ElevationMap(self.file_input)
        low_points = [pt for pt, ht in map.grid.items() if ht == ord('a')]
        print(len(low_points))

        for start_pt in low_points:
            path = map.find_shortest_path(start_pt)
            if not path:
                continue

            steps = len(path) - 1
            print(start_pt, steps)
            path_steps.append(steps)

        return min(path_steps)

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
print("test 2 solution: {}".format(solution.test2))
print("pt 1 solution: {}".format(solution.first))
print("pt 2 solution: {}".format(solution.second))
