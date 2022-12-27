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


class Expedition:
    @staticmethod
    def prune_redundancies(expeditions):
        uniques = []
        redundancies = {}

        for expedition in expeditions:
            key = (expedition.minute, expedition.pt)
            if key in redundancies:
                redundancies[key].append(expedition)
            else:
                redundancies[key] = [expedition]

        for expeditions in redundancies.values():
            uniques.append(expeditions[0])

        return uniques

    @staticmethod
    def find_fastest_expedition(valley_map):
        max_steps = math.inf
        fastest_expedition = None
        completed = []
        pruned = 0
        lf = 1000  # log frequency
        n = 0

        first_expedition = Expedition([valley_map.start_pt], valley_map)
        queue = [first_expedition]

        while queue:
            n += 1

            # Prune redundant
            if n % 100 == 0:
                before = len(queue)
                queue = Expedition.prune_redundancies(queue)
                print('trashed/left', before - len(queue), len(queue)) if n % lf == 0 else None

            expedition = queue.pop(0)
            print(n, expedition.minute, len(queue), pruned, max_steps) if n % lf == 0 else None

            for pt in expedition.possible_moves:
                alt_expedition = expedition.clone_expedition_at_next_pt(pt)

                if alt_expedition.at_goal:
                    completed.append(alt_expedition)
                    if not fastest_expedition or alt_expedition.steps < max_steps:
                        fastest_expedition = alt_expedition
                        max_steps = fastest_expedition.steps
                elif alt_expedition.steps < max_steps:
                    queue.append(alt_expedition)
                else:
                    pruned += 1

        print('first, completed, pruned', fastest_expedition, len(completed), pruned)
        return fastest_expedition

    def __init__(self, route, valley_map):
        self.route = route
        self.valley = valley_map

    @property
    def pt(self):
        return self.route[-1]

    @property
    def at_goal(self):
        return self.pt == self.valley.end_pt

    @property
    def minute(self):
        return self.steps

    @property
    def steps(self):
        return len(self.route) - 1

    @property
    def distance_to_end(self):
        x0, y0 = self.pt
        x1, y1 = self.valley.end_pt
        return abs(x1-x0) + abs(y1-y0)

    @property
    def possible_moves(self):
        pts = []

        for npt in self.neighbor_pts:
            if self.pt_will_be_open(npt):
                pts.append(npt)

        if self.pt_will_be_open(self.pt):
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

    def pt_will_be_open(self, pt):
        weather = self.valley.forecast_pt(pt, self.minute + 1)
        return len(weather) < 1

    def clone_expedition_at_next_pt(self, next_pt):
        clone = Expedition(list(self.route), self.valley)
        clone.move_to(next_pt)
        return clone

    def move_to(self, pt):
        self.route.append(pt)

    def __repr__(self):
        return f"<Expedition pt={self.pt} steps={self.steps}>"


class DismayedExpedition(Expedition):
    @staticmethod
    def prune_redundancies(expeditions):
        uniques = []
        redundancies = {}

        for expedition in expeditions:
            # Add leg to avoid confusing expeditions going different directions
            key = (expedition.leg, expedition.minute, expedition.pt)
            if key in redundancies:
                redundancies[key].append(expedition)
            else:
                redundancies[key] = [expedition]

        for expeditions in redundancies.values():
            uniques.append(expeditions[0])

        return uniques

    @staticmethod
    def find_fastest_expedition(valley_map):
        max_steps = math.inf
        fastest_expedition = None
        completed = []
        pruned = 0
        lf = 10000  # log frequency
        n = 0

        first_expedition = DismayedExpedition([valley_map.start_pt], valley_map)
        queue = [first_expedition]

        while queue:
            n += 1

            # Prune redundant
            if n % 1000 == 0:
                before = len(queue)
                queue = DismayedExpedition.prune_redundancies(queue)
                pruned += before - len(queue)
                print('trashed/left', before - len(queue), len(queue)) if n % lf == 0 else None

            expedition = queue.pop(0)
            print(n, expedition, len(queue), pruned) if n % lf == 0 else None

            for pt in expedition.possible_moves:
                alt_expedition = expedition.clone_expedition_at_next_pt(pt)

                if alt_expedition.at_goal:
                    if alt_expedition.leg == 3:
                        completed.append(alt_expedition)
                        if not fastest_expedition or alt_expedition.steps < max_steps:
                            fastest_expedition = alt_expedition
                            max_steps = fastest_expedition.steps
                    else:
                        alt_expedition.next_leg()
                        queue.append(alt_expedition)
                elif alt_expedition.steps < max_steps:
                    queue.append(alt_expedition)
                else:
                    pruned += 1

        print('first, completed, pruned', fastest_expedition, len(completed), pruned)
        return fastest_expedition

    def __init__(self, route, valley_map, leg=1):
        super().__init__(route, valley_map)
        self.start_pt = valley_map.start_pt if leg % 2 == 1 else valley_map.end_pt
        self.end_pt = valley_map.end_pt if leg % 2 == 1 else valley_map.start_pt
        self.leg = leg

    @property
    def at_goal(self):
        return self.pt == self.end_pt

    @property
    def possible_moves(self):
        pts = []

        for npt in self.neighbor_pts:
            if self.pt_will_be_open(npt):
                pts.append(npt)

        if self.pt_will_be_open(self.pt):
            pts.append(self.pt)

        if self.end_pt in pts:
            return [self.end_pt]
        else:
            return pts

    def next_leg(self):
        self.leg += 1
        self.start_pt, self.end_pt = self.end_pt, self.start_pt

    def clone_expedition_at_next_pt(self, next_pt):
        clone = DismayedExpedition(list(self.route), self.valley, self.leg)
        clone.move_to(next_pt)
        return clone

    def __repr__(self):
        return f"<Expedition pt={self.pt} end_pt={self.end_pt} steps={self.steps} leg={self.leg}>"


class ValleyMap:
    def __init__(self, ascii_map):
        self.ascii_map = ascii_map

    @cached_property
    def distance(self):
        x0, y0 = self.start_pt
        x1, y1 = self.end_pt
        return abs(x1-x0) + abs(y1-y0)

    @cached_property
    def start_pt(self):
        y = 0
        x = self.rows[y].index('.')
        return (x, y)

    @cached_property
    def end_pt(self):
        y = self.max_y
        x = self.rows[y].index('.')
        return (x, y)

    @cached_property
    def rows(self):
        rows = []
        for line in self.ascii_map.split('\n'):
            if line.strip() == '':
                continue
            row = list(line)
            rows.append(row)
        return rows

    @cached_property
    def cols(self):
        cols = []
        for x in range(len(self.rows[0])):
            col = []
            for row in self.rows:
                col.append(row[x])
            cols.append(col)
        return cols

    @cached_property
    def max_x(self):
        return len(self.cols) - 1

    @cached_property
    def max_y(self):
        return len(self.rows) - 1

    def pt_in_bounds(self, pt):
        x, y = pt
        if x < 1 or x >= self.max_x:
            return False
        if y < 1 or y >= self.max_y:
            return False
        return True

    def forecast_pt(self, pt, minute):
        chrs = []
        x, y = pt

        if pt in (self.start_pt, self.end_pt):
            return []

        if not self.pt_in_bounds(pt):
            return ['#']

        row = self.rows[y]
        col = self.cols[x]
        inner_row = row[1:-1]
        inner_col = col[1:-1]
        inner_x = x - 1
        inner_y = y - 1

        back_offset_x = abs(inner_x - minute) % len(inner_row)
        back_offset_y = abs(inner_y - minute) % len(inner_col)

        fwd_x = (inner_x + minute) % len(inner_row)
        bck_x = inner_x - minute if inner_x - minute >= 0 \
            else (len(inner_row) - back_offset_x) % len(inner_row)
        fwd_y = (inner_y + minute) % len(inner_col)
        bck_y = inner_y - minute if inner_y - minute >= 0 \
            else (len(inner_col) - back_offset_y) % len(inner_col)

        if inner_row[fwd_x] == '<':
            chrs.append('<')
        if inner_row[bck_x] == '>':
            chrs.append('>')
        if inner_col[fwd_y] == '^':
            chrs.append('^')
        if inner_col[bck_y] == 'v':
            chrs.append('v')

        return chrs


class Solution:
    def __init__(self, input_file):
        self.input_file = input_file

    #
    # Solutions
    #
    @property
    def test1(self):
        # Input
        ascii_map = TEST_INPUT

        # Vally Map Tests
        valley = ValleyMap(ascii_map)
        forecast = valley.forecast_pt((2, 1), 2)
        assert forecast == ['<', 'v'], forecast
        forecast = valley.forecast_pt((1, 0), 3)
        assert forecast == [], forecast
        forecast = valley.forecast_pt((1, 1), 4)
        assert forecast == [], forecast

        # Expedition
        valley_map = ValleyMap(ascii_map)
        print(valley_map.start_pt, valley_map.end_pt)
        fastest_expedition = Expedition.find_fastest_expedition(valley_map)
        assert fastest_expedition.steps == 18
        return fastest_expedition.steps

    @property
    def first(self):
        ascii_map = self.file_input
        valley_map = ValleyMap(ascii_map)
        print(valley_map.start_pt, valley_map.end_pt)
        fastest_expedition = Expedition.find_fastest_expedition(valley_map)
        return fastest_expedition.steps

    @property
    def test2(self):
        ascii_map = TEST_INPUT
        valley_map = ValleyMap(ascii_map)
        fastest_expedition = DismayedExpedition.find_fastest_expedition(valley_map)
        assert fastest_expedition.steps == 54
        return fastest_expedition.steps

    @property
    def second(self):
        ascii_map = self.file_input
        valley_map = ValleyMap(ascii_map)
        fastest_expedition = DismayedExpedition.find_fastest_expedition(valley_map)
        return fastest_expedition.steps

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
# Main
#
solution = Solution(INPUT_FILE)
print("test 1 solution: {}".format(solution.test1))
print("pt 1 solution: {}".format(solution.first))
print("test 2 solution: {}".format(solution.test2))
print("pt 2 solution: {}".format(solution.second))
