"""
Advent of Code 2021 - Day 15
https://adventofcode.com/2021/day/15
"""
from os.path import join as path_join
from functools import cached_property
from config import INPUT_DIR


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
    def first():
        pass

    @staticmethod
    def second():
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
    def test_input(self):
        return [l for l in TEST_MAP.split("\n") if l]

    #
    # Methods
    #
    def __init__(self, input_file):
        self.input_file = input_file


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
            _, (x, y) = open_paths.pop()

            if (x, y) == self.goal:
                break

            for neighbor in self.neighbors(x, y):
                cost = costs[(x, y)] + self.risk_values[(x, y)]
                if neighbor not in costs or cost < costs[neighbor]:
                    costs[neighbor] = cost
                    est_cost = cost + self.est_future_cost(neighbor)
                    open_paths.append((est_cost, neighbor))
                    open_paths.sort(reverse=True)
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
print("test: {}".format(Solution.test()))
print("pt 1 solution: {}".format(Solution.first()))
print("pt 2 solution: {}".format(Solution.second()))
