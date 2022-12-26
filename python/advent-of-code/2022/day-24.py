"""
Advent of Code 2022 - Day 24
https://adventofcode.com/2022/day/24
"""
from os.path import join as path_join
from functools import cached_property
from config import INPUT_DIR

import math
import pickle


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
    minute_cache = {}  # minute: instance

    @staticmethod
    def load_ascii_map(ascii_map):
        # Reset cache
        Valley.minute_cache = {}

        state = {}
        rows = [row for row in ascii_map.split('\n') if row.strip() != '']

        for y, line in enumerate(rows):
            cells = list(line)
            for x, pt_state in enumerate(cells):
                pt = (x, y)
                state[pt] = [pt_state]

        return Valley.from_cache(0, state)

    @staticmethod
    def from_cache(minute, state):
        if minute in Valley.minute_cache:
            #print('valley cache hit', minute) if minute % 10 == 0 else None
            return pickle.loads(Valley.minute_cache[minute])
        else:
            valley = Valley(state)
            Valley.minute_cache[minute] = pickle.dumps(valley)
            print('caching valley at min', minute)
            return valley

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
        pts.discard(self.start_pt)
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
        self.pts = self.next_pts.copy()

    def __repr__(self):
        return f"<Front dir='{self.direction}' pts={self.pts}>"


class TestExpedition:
    @staticmethod
    def find_fastest_expedition(valley):
        max_steps = math.inf
        fastest_expedition = None
        first_expedition = TestExpedition([valley.start_pt], valley.state)
        queue = [first_expedition]
        completed = []
        pruned = []
        n = 0

        while queue:
            n += 1
            expedition = queue.pop(0)
            #print(n, len(queue), len(expedition.valley.fronts))
            next_moves = expedition.possible_moves
            #print(n, len(queue), len(pruned), max_steps, fastest_expedition, len(completed))
            #breakpoint() if n % 100 == 0 else None
            print(n, expedition.minute, len(queue), len(pruned), len(completed), max_steps) if n % 10 == 0 else None
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
        self.valley = Valley.from_cache(self.minute, valley_state)

    @property
    def at_goal(self):
        return self.pt == self.valley.end_pt

    @property
    def started(self):
        visited = set(self.route) - set([self.valley.start_pt])
        return len(visited) > 0

    @property
    def minute(self):
        return self.steps

    @property
    def steps(self):
        return len(self.route) - 1

    @property
    def pt(self):
        return self.route[-1]

    @property
    def possible_moves(self):
        pts = []
        free_pts = self.valley.next_free_pts.copy()
        if self.started:
            free_pts.discard(self.valley.start_pt)

        for npt in self.neighbor_pts:
            if npt in free_pts:
                pts.append(npt)

        if self.pt in free_pts:
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
        clone = TestExpedition(list(self.route), self.valley.state)
        clone.move_to(next_pt)
        clone.valley.tick()
        return clone

    def move_to(self, pt):
        self.route.append(pt)

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
        return f"<TestExpedition pt={self.pt} steps={self.steps}>"


class Expedition(TestExpedition):
    @staticmethod
    def find_fastest_expedition(valley_map):
        max_steps = math.inf
        fastest_expedition = None
        first_expedition = Expedition([valley_map.start_pt], valley_map)
        queue = [first_expedition]
        completed = []
        pruned = 0
        n = 0
        queue_max = 10000

        while queue:
            n += 1

            # Prune redundant
            if n % 100 == 0:
                redundancies = {}
                for e in queue:
                    key = (e.minute, e.pt)
                    if key in redundancies:
                        redundancies[key].append(e)
                    else:
                        redundancies[key] = [e]

                uniques = []
                for es in redundancies.values():
                    uniques.append(es[0])

                trashed = len(queue) - len(uniques)
                print('trashed/left', trashed, len(uniques))
                pruned += trashed

                queue = uniques

            # Stop slowest expeditions
            if len(queue) > queue_max:
                pruned += len(queue) - queue_max
                queue = sorted(queue, key=lambda e: e.distance_to_end)
                print('pruning (fastest, mid, slowest)', queue[0], queue[math.floor(len(queue)/2)], queue[-1]) if n % 100 == 0 else None
                queue = queue[:queue_max]

            expedition = queue.pop(0)
            #print(n, len(queue), len(expedition.valley.fronts))
            next_moves = expedition.possible_moves
            #print(n, len(queue), len(pruned), max_steps, fastest_expedition, len(completed))
            #breakpoint() if n % 100 == 0 else None
            print(n, expedition.minute, [expedition.pt, '->', valley_map.end_pt], len(queue), pruned, len(completed), max_steps) if n % 100 == 0 else None
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
                    pruned += 1

        return fastest_expedition

    def __init__(self, route, valley_map):
        self.route = route
        self.valley = valley_map

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

    def clone_expedition_at_next_pt(self, next_pt):
        clone = Expedition(list(self.route), self.valley)
        clone.move_to(next_pt)
        return clone

    def pt_will_be_open(self, pt):
        # After minute 3 no going back to start
        if self.minute > 3 and pt == self.valley.start_pt:
             return False

        weather = self.valley.forecast_pt(pt, self.minute + 1)
        return len(weather) < 1

    def __repr__(self):
        return f"<Expedition pt={self.pt} steps={self.steps}>"


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
        bck_x = inner_x - minute if inner_x - minute >= 0 else (len(inner_row) - back_offset_x) % len(inner_row)
        fwd_y = (inner_y + minute) % len(inner_col)
        bck_y = inner_y - minute if inner_y - minute >= 0 else (len(inner_col) - back_offset_y) % len(inner_col)

        #print(pt, minute, fwd_x, bck_x, fwd_y, bck_y)
        #print(inner_col, fwd_y, bck_y)
        #print(inner_row, inner_row[fwd_x], inner_row[bck_x])
        #print(inner_col, inner_col[fwd_y], inner_col[bck_y])

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
        # Test Expedition
        valley = Valley.load_ascii_map(ascii_map)
        fastest_expedition = TestExpedition.find_fastest_expedition(valley)
        assert fastest_expedition.steps == 18
        print(fastest_expedition)

        # Expedition
        valley_map = ValleyMap(ascii_map)
        print(valley_map.start_pt, valley_map.end_pt)
        fastest_expedition = Expedition.find_fastest_expedition(valley_map)
        assert fastest_expedition.steps == 18

        breakpoint()

    @property
    def first(self):
        ascii_map = self.file_input
        valley_map = ValleyMap(ascii_map)
        print(valley_map.start_pt, valley_map.end_pt)
        fastest_expedition = Expedition.find_fastest_expedition(valley_map)
        return fastest_expedition.steps

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
