"""
Advent of Code 2021 - Day 15
https://adventofcode.com/2021/day/15
"""
from os.path import join as path_join
from functools import cached_property
from config import INPUT_DIR
import heapq


INPUT_FILE = path_join(INPUT_DIR, 'day-15.txt')
TEST_MAP = """\
1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581
"""


class Solution:
    #
    # Solutions
    #
    @staticmethod
    def test():
        expected = 40

        solution = Solution(None)
        path_finder = PathFinder(solution.test_input)
        path_risk = path_finder.sum_lowest_risk_path()

        assert path_risk == expected, (path_risk, expected)
        return 'PASS'

    @staticmethod
    def test2():
        expected = 315

        solution = Solution(None)
        assert len(solution.extended_test_input) == 50, len(solution.extended_test_input)
        assert len(solution.extended_test_input[0]) == 50, len(solution.extended_test_input[0])
        assert solution.extended_test_input[-1][-10:] == '1299833479'

        path_finder = PathFinder(solution.extended_test_input)
        path_risk = path_finder.sum_lowest_risk_path()

        assert path_risk == expected, (path_risk, expected)
        return 'PASS'

    @staticmethod
    def first():
        solution = Solution(INPUT_FILE)
        path_finder = PathFinder(solution.input_lines)
        path_risk = path_finder.sum_lowest_risk_path()
        return path_risk

    @staticmethod
    def second():
        solution = Solution(INPUT_FILE)
        path_finder = PathFinder(solution.extended_input_lines)
        path_risk = path_finder.sum_lowest_risk_path()
        return path_risk

    #
    # Properties
    #
    @cached_property
    def input_lines(self):
        with open(self.input_file) as file:
            lines = file.readlines()
            return [line.strip() for line in lines]

    @cached_property
    def extended_input_lines(self):
        top_left_tile = self.input_lines.copy()
        return self.extend_map(top_left_tile)

    @cached_property
    def test_input(self):
        return [l for l in TEST_MAP.split("\n") if l]

    @cached_property
    def extended_test_input(self):
        top_left_tile = self.test_input.copy()
        return self.extend_map(top_left_tile)

    #
    # Methods
    #
    def __init__(self, input_file):
        self.input_file = input_file

    def extend_map(self, top_left_tile):
        extended_rows = []

        for n in range(5):
            for row in top_left_tile:
                new_row = [int(risk) % 9 + n for risk in row]
                extended_row = self.extend_row(new_row)
                extended_rows.append(extended_row)

        return extended_rows

    def extend_row(self, row):
        extended_row = []

        for n in range(5):
            for risk in row:
                new_risk = (risk + n) % 9
                if new_risk == 0: new_risk = 9
                extended_row.append(str(new_risk))

        return ''.join(extended_row)


class PathFinder:
    def __init__(self, map_rows):
        self.map_rows = map_rows

    @cached_property
    def start(self):
        """Upper left"""
        return (0, 0)

    @cached_property
    def goal(self):
        """Lower right"""
        return (self.grid_width - 1, self.grid_height - 1)

    @cached_property
    def grid_width(self):
        return len(self.map_rows[0])

    @cached_property
    def grid_height(self):
        return len(self.map_rows)

    @cached_property
    def risk_values(self):
        grid = {}
        for y, row in enumerate(self.map_rows):
            for x, risk in enumerate(list(row)):
                grid[(x, y)] = int(risk)
        return grid

    def sum_lowest_risk_path(self):
        path = self.find_lowest_risk_path()
        return sum([self.risk_values[pt] for pt in path if pt != self.start])

    def find_lowest_risk_path(self):
        """Source:
        https://github.com/llimllib/personal_code/blob/master/misc/advent/2021/15/d.py
        """
        open_paths = [(0, self.start)]
        steps = {self.start: None}
        costs = {self.start: 0}

        while open_paths:
            _, (x, y) = heapq.heappop(open_paths)

            if (x, y) == self.goal:
                break

            for neighbor in self.neighbors(x, y):
                cost = costs[(x, y)] + self.risk_values[(x, y)]
                if neighbor not in costs or cost < costs[neighbor]:
                    costs[neighbor] = cost
                    heapq.heappush(open_paths, (cost, neighbor))
                    steps[neighbor] = (x, y)

        return self.steps_to_path(steps)

    def steps_to_path(self, steps):
        path = [self.goal]
        step = steps[self.goal]
        while step:
            path.append(step)
            step = steps[step]
        return reversed(path)

    def neighbors(self, x, y):
        if x > 0:
            yield (x - 1, y)
        if x < self.grid_width - 1:
            yield (x + 1, y)
        if y > 0:
            yield (x, y - 1)
        if y < self.grid_height - 1:
            yield (x, y + 1)

    def est_future_cost(self, pt):
        x, y = pt
        return abs(self.goal[0] - x) + abs(self.goal[1] - y)


#
# Main
#
print("test 1: {}".format(Solution.test()))
print("test 2: {}".format(Solution.test2()))
print("pt 1 solution: {}".format(Solution.first()))
print("pt 2 solution: {}".format(Solution.second()))
