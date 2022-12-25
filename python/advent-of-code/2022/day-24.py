"""
Advent of Code 2022 - Day 24
https://adventofcode.com/2022/day/24
"""
from os.path import join as path_join
from functools import cached_property
from config import INPUT_DIR

import math


INPUT_FILE = path_join(INPUT_DIR, 'day-24.txt')

TEST_INPUT = """\
#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#"""

DIRS = '^>v<'


class Valley:
    @staticmethod
    def load_ascii_map(ascii_map):
        state = {}
        rows = [row for row in ascii_map.split('\n') if row.strip() != '']

        for y, line in enumerate(rows):
            cells = list(line)
            for x, pt_state in enumerate(cells):
                pt = (x, y)
                state[pt] = [pt_state]

        return Valley(state)

    def __init__(self, state):
        self.pts = set(state.keys())
        self.start_pt = self.extract_start_pt(state)
        self.end_pt = self.extract_end_pt(state)
        self.fronts = self.extract_fronts(state)

    @property
    def state(self):
        state = {}
        for pt in self.pts:
            pt_state = []
            if pt in (self.start_pt, self.end_pt):
                pt_state.append('.')
            elif pt in self.wall_pts:
                pt_state.append('#')
            else:
                for front in self.fronts:
                    if pt in front.pts:
                        pt_state.append(front.direction)
            state[pt] = pt_state
        return state

    @cached_property
    def max_x(self):
        return max(x for x, _ in self.pts)

    @cached_property
    def max_y(self):
        return max(y for _, y in self.pts)

    @cached_property
    def wall_pts(self):
        pts = set()
        for x, y in self.pts:
            if x in (0, self.max_x):
                pts.add((x, y))
            elif y in (0, self.max_y):
                pts.add((x, y))
        pts.discard(self.end_pt)
        return pts

    @cached_property
    def floor_pts(self):
        return self.pts - self.wall_pts

    @property
    def free_pts(self):
        free_pts = self.floor_pts.copy()
        for pt in self.floor_pts:
            for front in self.fronts:
                if pt in front.pts:
                    free_pts.discard(pt)
        return free_pts

    @property
    def next_free_pts(self):
        free_pts = self.floor_pts.copy()
        for pt in self.floor_pts:
            for front in self.fronts:
                if pt in front.next_pts:
                    free_pts.discard(pt)
        return free_pts

    @property
    def ascii_map(self):
        lines = []
        for y in range(0, self.max_y+1):
            line = []
            for x in range(0, self.max_x+1):
                pt = (x, y)
                chrs = self.state[pt]
                if not chrs:
                    chr = '.'
                elif len(chrs) == 1:
                    chr = chrs[0]
                else:
                    chr = str(len(chrs))
                line.append(chr)
            lines.append(''.join(line))
        return "\n".join(lines)

    def tick(self):
        for front in self.fronts:
            front.move()
        return self.ascii_map

    def extract_start_pt(self, state):
        for (x, y), chrs in state.items():
            if y == 0 and '.' in chrs:
                return (x, y)

    def extract_end_pt(self, state):
        for (x, y), chrs in state.items():
            if y == self.max_y and '.' in chrs:
                return (x, y)

    def extract_fronts(self, state):
        fronts = []
        max_xy = (self.max_x-1, self.max_y-1)

        # N/S Fronts (^v)
        for y in range(0, self.max_y):
            for dir in ('^', 'v'):
                pts = set()
                for x in range(0, self.max_x):
                    pt = (x, y)
                    chrs = state[pt]
                    if dir in chrs:
                        pts.add(pt)
                if pts:
                    front = BlizzardFront(dir, pts, max_xy)
                    fronts.append(front)

        # E/W Front (><)
        for x in range(0, self.max_x):
            for dir in ('>', '<'):
                pts = set()
                for y in range(0, self.max_y):
                    pt = (x, y)
                    chrs = state[pt]
                    if dir in chrs:
                        pts.add(pt)
                if pts:
                    front = BlizzardFront(dir, pts, max_xy)
                    fronts.append(front)

        return fronts


class BlizzardFront:
    def __init__(self, direction, pts, max_xy):
        self.direction = direction
        self.pts = pts
        self.max_x = max_xy[0]
        self.max_y = max_xy[1]

    @property
    def next_pts(self):
        pts = self.pts.copy()
        x1, y1 = list(self.pts)[0]

        if self.direction == 'v':
            yn = y1+1 if y1 < self.max_y else 1
            pts = [(x, yn) for x, y in pts]
        elif self.direction == '>':
            xn = x1+1 if x1 < self.max_x else 1
            pts = [(xn, y) for x, y in pts]
        elif self.direction == '^':
            yn = y1-1 if y1 > 1 else self.max_y
            pts = [(x, yn) for x, y in pts]
        else:
            xn = x1-1 if x1 > 1 else self.max_x
            pts = [(xn, y) for x, y in pts]

        return pts

    def move(self):
        self.pts = self.next_pts

    def __repr__(self):
        return f"<Front dir='{self.direction}' pts={self.pts}>"


class Expedition:
    @staticmethod
    def find_fastest_expedition(valley):
        max_steps = math.inf
        fastest_expedition = None
        first_expedition = Expedition([valley.start_pt], valley.state)
        queue = [first_expedition]
        completed = []
        pruned = []
        n = 0

        while queue:
            n += 1
            expedition = queue.pop(0)
            next_moves = expedition.possible_moves
            #print(n, len(queue), len(pruned), max_steps, fastest_expedition, len(completed))
            #breakpoint() if n % 100 == 0 else None
            print(n, len(queue), len(pruned), len(completed), max_steps) if n % 100 == 0 else None
            for pt in next_moves:
                alt_expedition = expedition.clone_expedition_at_next_pt(pt)

                if alt_expedition.at_goal:
                    completed.append(alt_expedition)
                    #print(alt_expedition.route)
                    if not fastest_expedition or alt_expedition.steps < max_steps:
                        fastest_expedition = alt_expedition
                        max_steps = fastest_expedition.steps
                elif alt_expedition.steps < max_steps:
                    queue.append(alt_expedition)
                else:
                    pruned.append(alt_expedition)

        return fastest_expedition

    def __init__(self, route, valley_state):
        self.route = route
        self.valley = Valley(valley_state)

    @property
    def at_goal(self):
        return self.pt == self.valley.end_pt

    @property
    def steps(self):
        return len(self.route) - 1

    @property
    def pt(self):
        return self.route[-1]

    @property
    def possible_moves(self):
        pts = []

        for npt in self.neighbor_pts:
            if npt in self.valley.next_free_pts:
                pts.append(npt)

        if self.pt in self.valley.next_free_pts:
            pts.append(self.pt)

        if self.valley.end_pt in pts:
            return [self.valley.end_pt]
        else:
            return pts

    @property
    def neighbor_pts(self):
        x, y = self.pt
        return [
            (x+1, y),
            (x, y+1),
            (x-1, y),
            (x, y-1)
        ]

    def clone_expedition_at_next_pt(self, next_pt):
        clone = Expedition(list(self.route), self.valley.state)
        clone.route.append(next_pt)
        clone.valley.tick()
        return clone

    @property
    def log(self):
        logs = []
        dir_map = {
            (-1, 0): 'left',
            (1, 0): 'right',
            (0, 1): 'down',
            (0, -1): 'up',
            (0, 0): 'wait',
        }

        for n, pt in enumerate(self.route):
            x, y = pt
            if n == 0:
                log = (0, 'initial state', pt)
            else:
                px, py = self.route[n-1]
                diff = (x-px, y-py)
                dir = dir_map[diff]
                log = (n, dir, pt)
            logs.append(log)
        return logs


    def __repr__(self):
        return f"<Expedition pt={self.pt} steps={self.steps}>"


class Solution:
    def __init__(self, input_file):
        self.input_file = input_file

    #
    # Solutions
    #
    @property
    def test1(self):
        ascii_map = TEST_INPUT
        valley = Valley.load_ascii_map(ascii_map)
        expected_free_pts = [(1, 2), (3, 1), (3, 2), (3, 3), (4, 2), (6, 5)]
        assert valley.start_pt == (1, 0), valley.start_pt
        assert valley.end_pt == (6, 5), valley.end_pt
        assert len(valley.free_pts) == len(expected_free_pts), f"expect 5 got {valley.free_pts}"
        assert len(set(expected_free_pts) - valley.free_pts) == 0

        fastest_expedition = Expedition.find_fastest_expedition(valley)
        print(fastest_expedition)
        return fastest_expedition.steps

    @property
    def first(self):
        ascii_map = self.file_input

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
