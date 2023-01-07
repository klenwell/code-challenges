"""
Advent of Code 2022 - Day 17
https://adventofcode.com/2022/day/17
"""
from os.path import join as path_join
from functools import cached_property
from config import INPUT_DIR

import time


INPUT_FILE = path_join(INPUT_DIR, 'day-17.txt')

TEST_INPUT = """\
>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"""

ROCK_PATTERNS = """\
####

.#.
###
.#.

..#
..#
###

#
#
#
#

##
##"""

ROCK_SYMBOLS = ['—', '+', '⅃', '|', '■']

PUFF_OFFSET = {
    '>': 1,
    '<': -1
}


class Rock:
    def __init__(self, number):
        self.number = number
        self.x = 0
        self.y = 0

    @property
    def pattern(self):
        i = self.number % len(ROCK_SYMBOLS)
        types = ROCK_PATTERNS.split('\n\n')
        return types[i]

    @property
    def symbol(self):
        i = self.number % len(ROCK_SYMBOLS)
        return ROCK_SYMBOLS[i]

    @property
    def pt(self):
        return (self.x, self.y)

    def set_pt(self, pt):
        self.x, self.y = pt
        return self

    @property
    def pts(self):
        pts = set()
        for y, row in enumerate(reversed(self.rows)):
            for x, char in enumerate(row):
                if char == '#':
                    pts.add((self.x+x, self.y+y))
        return pts

    def overlaps(self, other):
        #print('collision', self.pts.intersection(other.pts), self.pts, other.pts)
        return len(self.pts.intersection(other.pts)) > 0

    @cached_property
    def rows(self):
        rows = []
        for line in self.pattern.split('\n'):
            row = list(line)
            rows.append(row)
        return rows

    @cached_property
    def width(self):
        return max([len(row) for row in self.rows])

    @cached_property
    def height(self):
        return len(self.rows)

    @property
    def max_x(self):
        return self.x + self.width

    @property
    def max_y(self):
        return self.y + self.height

    def __repr__(self):
        return f"<Rock #{self.number} {self.symbol} ({self.x}, {self.y})>"


class DroppedRock:
    def __init__(self, rock, previous_dropped_rock, puff_seq):
        self.rock = rock
        self.previous_dropped = previous_dropped_rock
        self.puff_seq = tuple(puff_seq)

    @property
    def pt(self):
        return self.rock.pt

    @property
    def x(self):
        return self.rock.x

    @property
    def y(self):
        return self.rock.y

    @property
    def pts(self):
        return self.rock.pts

    @property
    def dy(self):
        # Effectivly pile height change.
        return self.y - self.previous_dropped.y

    @property
    def key(self):
        return (self.rock.symbol, self.puff_seq, self.rock.x, self.dy)

    @property
    def puff_stream(self):
        return ''.join(self.puff_seq)

    def __repr__(self):
        return f"<DroppedRock {self.rock.symbol} {self.pt} puffs={self.puff_stream}>"


class Stratum:
    @staticmethod
    def from_chamber(chamber):
        return Stratum(chamber.last_rock_cycle, chamber.height)

    def __init__(self, dropped_rocks, y):
        # y is the total rock pile height, which could be higher than any rocks in
        # stratum group
        self.dropped_rocks = dropped_rocks
        self.y = y

    def cycles(self, previous_stratum):
        if not previous_stratum:
            return False

        if self.key != previous_stratum.key:
            return False

        return True

    @property
    def key(self):
        rock_keys = []
        for rock in self.dropped_rocks:
            rock_keys.append(rock.key)
        return tuple(rock_keys)

    @property
    def puff_stream(self):
        return ''.join([dr.puff_stream for dr in self.dropped_rocks])

    @property
    def rock_pile(self):
        return ''.join([dr.rock.symbol for dr in self.dropped_rocks])

    @property
    def height(self):
        return sum(dr.rock.height for dr in self.dropped_rocks)

    @property
    def index(self):
        return (self.dropped_rocks[0].rock.number, self.dropped_rocks[-1].rock.number)

    def __repr__(self):
        pt = self.dropped_rocks[0].pt
        return f"<Stratum index={self.index} y={self.y} height={self.height}>"


class StrataCycle:
    def __init__(self, start_stratum, end_stratum, rocks_left):
        self.start_stratum = start_stratum
        self.end_stratum = end_stratum
        self.rocks_left = rocks_left

    @property
    def cycle_height(self):
        return self.end_stratum.y - self.start_stratum.y

    @property
    def cycle_rocks(self):
        return self.end_stratum.index[1] - self.start_stratum.index[0] + 1

    @property
    def cycle_strata(self):
        return self.cycle_rocks / len(self.end_stratum.dropped_rocks)

    @property
    def cycles(self):
        return self.rocks_left // self.cycle_rocks

    @property
    def rock_count(self):
        return self.cycle_rocks * self.cycles

    @property
    def strata_count(self):
        return self.cycle_strata * self.cycles

    @property
    def height(self):
        return self.cycles * self.cycle_height

    @property
    def ys(self):
        return (self.start_stratum.dropped_rocks[0].y, self.end_stratum.dropped_rocks[-1].y)

    @property
    def index(self):
        return (self.start_stratum.index[0], self.end_stratum.index[1])

    def __repr__(self):
        strata = int(self.strata_count)
        rocks = self.rock_count
        return f"<StrataCycle index={self.index} strata={strata} rocks={rocks} height={self.height}>"


class TetrisChamber:
    def __init__(self, width, jet_pattern):
        self.width = width
        self.jet_queue = list(jet_pattern)

        self.dropped_rocks = []
        self.strata = []
        self.strata_index = {}
        self.pts = set()

        # See cycle_is_detected method below.
        self.cycle_index = {}
        self.cycle_queue = []

        self.bottom_y = 0

        self.start_x = 2
        self.start_y = 4

    def drop_rocks(self, num):
        rocks_left = num
        cycled_strata = None

        while rocks_left > 0:
            rock = Rock(num - rocks_left)
            dropped_rock = self.drop_rock(rock)
            self.collect_rock(dropped_rock)
            rocks_left -= 1

            print('dropped rock', rock) #if rocks_left % 1000 == 0 else None

            if rocks_left > len(self.jet_queue) and self.cycle_is_detected():
            #if self.cycle_is_detected():
                end_stratum = self.last_stratum
                start_stratum = self.strata_index.get(end_stratum.key)
                cycled_strata = StrataCycle(start_stratum, end_stratum, rocks_left)
                rocks_left = num - cycled_strata.rock_count - len(self.dropped_rocks)
                print('cycle_is_detected', (rock.number, rocks_left), cycled_strata, self)

        print('no mo rox', self, cycled_strata)
        breakpoint()

        if cycled_strata:
            print('cycled_strata', self.height, cycled_strata.height, self.height + cycled_strata.height)
            return self.height + cycled_strata.height
        else:
            return self.height

    def cycle_is_detected(self):
        # Only check for cycle if we've cycled at least one through jet queue.
        if len(self.strata) < len(self.jet_queue):
            return False

        end_stratum = self.last_stratum
        start_stratum = self.strata_index.get(end_stratum.key)

        if end_stratum.cycles(start_stratum):
            #print('cycle_is_detected', identical_stratum, self.last_stratum)
            return True
        else:
            self.strata_index[self.last_stratum.key] = self.last_stratum
            return False

    def collect_rock(self, dropped_rock):
        self.dropped_rocks.append(dropped_rock)

        if not self.last_rock_cycle:
            return None

        stratum = Stratum.from_chamber(self)
        self.strata.append(stratum)
        return stratum

    def compute_cyclical_strata_chunk(self, rocks_left):
        from collections import namedtuple
        StrataChunk = namedtuple('StrataChunk', ['cycles', 'rocks', 'height'])

        end_stratum = self.last_stratum
        start_stratum = self.strata_index.get(end_stratum.key)

        if not end_stratum.cycles(start_stratum):
            return None

        cycle_height = end_stratum.y - start_stratum.y
        cycle_rocks = end_stratum.index[1] - start_stratum.index[0]

        cycles = rocks_left // cycle_rocks
        chunk_rocks = cycle_rocks * cycles
        #print(2022 - chunk_rocks - len(self.dropped_rocks), rocks_left % cycle_rocks)
        chunk_height = cycles * cycle_height

        return StrataChunk(cycles, chunk_rocks, chunk_height)

    def drop_rock(self, rock):
        puffs = []
        rock.x = self.start_x
        rock.y = self.height + self.start_y
        dropping = True

        #print('rock start:', rock)
        while dropping:
            # After a rock appears, it alternates between being
            # pushed by a jet of hot gas one unit
            # (in the direction indicated by the next symbol in the jet pattern)
            init_x = rock.x
            puff = self.jet_queue.pop(0)
            rock.x += PUFF_OFFSET[puff]

            # If hits wall or resting rock, restore x
            if self.rock_hits_wall(rock) or rock.overlaps(self):
                rock.x = init_x

            puffs.append(puff)
            self.jet_queue.append(puff)

            # and then falling one unit down.
            rock.y -= 1

            # If any movement would cause any part of the rock to move into the walls, floor, or a stopped rock,
            # the movement instead does not occur.
            collision = rock.overlaps(self) or self.rock_hits_floor(rock)
            if collision:
                rock.y += 1  # restore to previous point
                break

        #     print('dropping:', rock)
        # print('rock stop:', rock)

        self.pts = self.pts.union(rock.pts)
        self.scan_surface_pts(self.pts)

        return DroppedRock(rock, self.last_dropped_rock, puffs)

    @property
    def last_dropped_rock(self):
        # If no rocks yet, represent floor as a rock
        if not self.dropped_rocks:
            floor = Rock(0)
            return floor
        else:
            return self.dropped_rocks[-1]

    @property
    def last_stratum(self):
        return self.strata[-1]

    @property
    def last_rock_cycle(self):
        cycle_len = len(ROCK_SYMBOLS) + 7
        rock_cycle = self.dropped_rocks[-cycle_len:]

        if len(rock_cycle) < cycle_len:
            return None
        else:
            return rock_cycle

    def old_cycle_is_detected(self, rock, puff_seq):
        rock_key = self.rock_key(rock, puff_seq)
        cycle_key = self.cycle_key(rock_key)

        if cycle_key in self.cycle_index:
            print('cycle_is_detected', rock, puff_seq)
            breakpoint()
            return True
        else:
            self.cycle_index[cycle_key] = self.height
            self.cycle_queue.append(rock_key)
            return False

    @property
    def last_rock(self):
        if not self.rocks:
            return None
        else:
            return self.rocks[-1]

    def rock_key(self, rock, puff_seq):
        dy = rock.y - self.last_rock.y if self.last_rock else rock.y
        return (rock.symbol, tuple(puff_seq), rock.x, dy)

    def cycle_key(self, rock_key):
        last_4_rocks = self.cycle_queue[-4:]
        return tuple(last_4_rocks) + (rock_key,)

    def scan_surface_pts(self, pts):
        # This is kinda slow so do it as infrequently as possible.
        if len(self.pts) < 500:
            return False

        # DFS
        surface_pts = set()
        start_pt = (0, self.height+1)
        queue = [start_pt]
        visited = []

        while queue:
            pt = queue.pop()
            visited.append(pt)

            for npt in self.neighbors(pt):
                if npt in self.pts:
                    surface_pts.add(npt)
                elif npt not in visited:
                    queue.append(npt)
            #print('scan_surface_pts', len(queue), surface_pts)

        self.pts = surface_pts
        return True

    def neighbors(self, pt):
        pts = []
        x, y = pt
        nsew = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        for (dx, dy) in nsew:
            nx = x + dx
            ny = y + dy
            #print('npt', pt, (nx, ny))
            if nx < 0 or nx >= self.width:
                continue
            if ny < self.bottom_y or ny > self.height+1:
                continue
            pts.append((nx, ny))
        #print(pts)
        return pts

    def rock_hits_wall(self, rock):
        return rock.x < 0 or rock.max_x > self.width

    def rock_hits_floor(self, rock):
        return rock.y <= self.bottom_y

    @property
    def height(self):
        if not self.pts:
            return self.bottom_y
        return max(y for _, y in self.pts)

    def __repr__(self):
        return f"<Chamber height={self.height} pts={len(self.pts)}>"


class Boulder(TetrisChamber):
    def __init__(self, width, jet_pattern):
        super().__init__(width, jet_pattern)

    def build(self):
        cycles = len(self.jet_queue) * 1000
        total_puffs = 0

        for n in range(cycles):
            type, symbol = self.rock_types[n % len(self.rock_types)]
            rock = Rock(type, symbol)

            puffs = self.drop_rock(rock)
            total_puffs += puffs

            print(n, cycles, total_puffs, self.chamber_is_sealed()) if n % 100 == 0 else None

            if self.cycle_detected(total_puffs):
                print('captured!', total_puffs)
                breakpoint()

        raise Exception(f"No cycle detected after {total_puffs} puffs")

    def cycle_detected(self, puffs):
        # if not self.chamber_is_sealed():
        #     return False

        #print(puffs, len(self.jet_queue), puffs % len(self.jet_queue), puffs % len(self.jet_queue) == 0)
        return puffs % len(self.jet_queue) == 0

    def chamber_is_sealed(self):
        for col in range(self.width):
            pts = [(x, y) for x,y in self.pts if x == col]
            if not pts:
                return False
        return True


class Solution:
    def __init__(self, input_file):
        self.input_file = input_file

    #
    # Solutions
    #
    @property
    def test1(self):
        jet_pattern = TEST_INPUT
        width = 7
        count = 2022

        self.test_rock()
        self.test_chamber()
        self.test_drop()

        chamber = TetrisChamber(width, jet_pattern)
        height = chamber.drop_rocks(count)
        assert height == 3068, (height, chamber)
        return height

    @property
    def first(self):
        jet_pattern = self.file_input
        width = 7
        count = 2022

        chamber = TetrisChamber(width, jet_pattern)
        height = chamber.drop_rocks(count)
        assert height == 3119, chamber
        return height

    @property
    def test2(self):
        jet_pattern = TEST_INPUT
        width = 7
        count = 1000000000000  # one trillion (or a million million)

        self.benchmark()
        self.test_floors()
        self.test_boulder()
        self.test_cycles()

        chamber = TetrisChamber(width, jet_pattern)
        height = chamber.drop_rocks(count)
        assert height == 1514285714288, chamber
        return height

    def benchmark(self):
        jet_pattern = TEST_INPUT
        width = 7
        count = 10000
        factor = 1000000000000 / count
        ten_mins = 10 * 60

        t0 = time.time()
        chamber = TetrisChamber(width, jet_pattern)
        height = chamber.drop_rocks(count)
        t1 = time.time() - t0

        est_secs = t1 * factor
        est_days = est_secs / (24 * 3600)
        est_years = est_days / 365

        best_result = [
            # seconds
            266337442,  # DFS surface pts
            3967672253  # Aggregate rock pts
        ][0]

        print('est time (secs, days, years):', est_secs, est_days, est_years)
        assert est_secs < best_result, f"Worse result (than {best_result})"
        assert est_secs < ten_mins, f"Will take more than 10 mins"

    def test_floors(self):
        jet_pattern = TEST_INPUT
        width = 7
        count = 1000000000000  # one trillion (or a million million)
        chamber = FastTetrisChamber(width, jet_pattern)
        floors = chamber.find_floors()
        breakpoint()

    def test_boulder(self):
        jet_pattern = TEST_INPUT
        width = 7
        count = 1000000000000  # one trillion (or a million million)

        mega_rock = Boulder(width, jet_pattern).build()

    def test_cycles(self):
        jet_pattern = TEST_INPUT
        width = 7
        count = 1000000000000  # one trillion (or a million million)

        print(len(jet_pattern), len(self.file_input))

        chamber = FastTetrisChamber(width, jet_pattern)
        chamber.drop_rocks(len(jet_pattern))
        top_y = chamber.height * -1

        for y in range(top_y, 0):
            floor = False
            for x in range(width):
                if (x, y) not in chamber.pts:
                    break
            if floor:
                print('floor level', y)

    @property
    def second(self):
        pass

    #
    # Tests
    #
    def test_rock(self):
        rock = Rock(1)
        assert rock.pt == (0, 0), rock
        assert rock.symbol == '+', rock
        assert rock.height == 3, rock
        assert rock.width == 3, rock
        assert len(rock.pts) == 5, rock
        print('test_rock passed')

    def test_chamber(self):
        chamber = TetrisChamber(7, TEST_INPUT)
        assert chamber.height == 0, chamber.height
        assert len(chamber.pts) == 0, chamber.pts
        print('test_chamber passed')

    def test_drop(self):
        dropped_rocks = []
        expected_rocks_pts = [
            (2, 1), (2, 2), (0, 4), (4, 4), (4, 8),
            (1, 10), (1, 11), (3, 13), (4, 14), (0, 13)
        ]

        chamber = TetrisChamber(7, TEST_INPUT)

        for n, expected_pt in enumerate(expected_rocks_pts):
            rock = Rock(n)
            dropped_rock = chamber.drop_rock(rock)
            dropped_rocks.append(dropped_rock)
            assert dropped_rock.pt == expected_pt, (n+1, expected_pt, dropped_rock)

        assert chamber.height == 17, (chamber, chamber.rocks, chamber.pts)
        print('test_drop passed')

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
