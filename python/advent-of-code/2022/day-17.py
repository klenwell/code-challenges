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

ROCK_TYPES = """\
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
    def __init__(self, pattern, symbol):
        self.pattern = pattern
        self.symbol = symbol
        self.x = 0
        self.y = 0

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
        return f"<Rock {self.symbol} ({self.x}, {self.y})>"


class TetrisChamber:
    def __init__(self, width, jet_pattern):
        self.width = width
        self.jet_queue = list(jet_pattern)

        self.rock_types = list(zip(ROCK_TYPES.split('\n\n'), ROCK_SYMBOLS))
        self.rocks = []
        self.pts = set()

        self.bottom_y = 0

        self.start_x = 2
        self.start_y = 4

    def drop_rocks(self, num):
        for n in range(num):
            type, symbol = self.rock_types[n % len(self.rock_types)]
            rock = Rock(type, symbol)

            print('drop rock', n+1) if n % 1000 == 0 else None
            self.drop_rock(rock)

        return self.height

    def drop_rock(self, rock):
        puffs = 0
        rock.x = self.start_x
        rock.y = self.height + self.start_y
        dropping = True

        #print('rock start:', rock)
        while dropping:
            puffs += 1
            rock = self.jet_push_rock(rock)
            rock.y -= 1
            collision = rock.overlaps(self) or self.rock_hits_floor(rock)

            if collision:
                rock.y += 1  # restore to previous point
                break
            #print('dropping:', rock)
        #print('rock stop:', rock)

        self.pts = self.pts.union(rock.pts)
        self.rocks.append(rock)
        return puffs

    def jet_push_rock(self, rock):
        init_x = rock.x

        puff = self.jet_queue.pop(0)
        rock.x += PUFF_OFFSET[puff]
        self.jet_queue.append(puff)
        #print(init_x, puff, PUFF_OFFSET[puff], rock.x)

        # If hits wall or resting rock, restore x
        if self.rock_hits_wall(rock) or rock.overlaps(self):
            #print('wall')
            rock.x = init_x

        return rock

    def rock_hits_wall(self, rock):
        return rock.x < 0 or rock.max_x > self.width

    def rock_hits_floor(self, rock):
        return rock.y <= self.bottom_y

    @property
    def height(self):
        if not self.rocks:
            return self.bottom_y
        return max(y for _, y in self.pts)

    def __repr__(self):
        return f"<Chamber height={self.height} rocks={len(self.rocks)}>"


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


class FastTetrisChamber(TetrisChamber):
    def __init__(self, width, jet_pattern):
        super().__init__(width, jet_pattern)
        self.floor_logs = []
        self.rocks = 0

    def detect_new_floors(self, rock):
        floors = []
        for y in range(rock.y, rock.max_y):
            if self.floor_at_y(y) == '#######':
                floors.append(y)
        return floors

    def next_rock(self, num):
        type, symbol = self.rock_types[num % len(self.rock_types)]
        return Rock(type, symbol)

    def floor_at_y(self, y):
        cubes = []
        for x in range(self.width):
            cube = '#' if (x, y) in self.pts else '.'
            cubes.append(cube)
        return ''.join(cubes)

    def show_rock(self, rock):
        floors = []
        for y in range(rock.y, rock.max_y):
            floor = list(self.floor_at_y(y))
            xs = [rx for rx, ry in rock.pts if ry == y]
            c = lambda x: '@' if x in xs else floor[x]
            cubes = [c(x) for x in range(len(floor))]
            floors.append(''.join(cubes))
        return '\n'.join(floors)

    def find_floors(self):
        for n in range(100000):
            t0 = time.time()
            rock = self.next_rock(n)
            self.drop_rock(rock)
            new_floors = self.detect_new_floors(rock)
            if new_floors:
                for y in new_floors:
                    self.floor_logs.append((y, n, rock))
                breakpoint()

            if n % 997 == 0:
                print('find_floors', n, rock.y, time.time()-t0, f"\n{self.show_rock(rock)}")
                self.clear_debris()
        return [y for y, _, _ in self.floor_logs]

    def drop_rocks(self, num):
        t0 = time.time()
        for n in range(num):
            rock = self.next_rock(n)

            print('drop rock', n+1, time.time()-t0, n*100/num) if n % 1000 == 0 else None
            self.drop_rock(rock)
            # print(rock, f"\n{self.show_rock(rock)}")
            # breakpoint() if n % 5 == 0 else None

        return self.height

    def drop_rock(self, rock):
        puffs = 0
        rock.x = self.start_x
        rock.y = self.bottom_y - self.height - rock.height + self.start_y
        dropping = True

        #print('rock start:', rock)
        while dropping:
            puffs += 1
            rock = self.jet_push_rock(rock)
            rock.y += 1
            collision = rock.overlaps(self) or self.rock_hits_floor(rock)

            if collision:
                rock.y -= 1  # restore to previous point
                break

            #print('dropping:', rock)
        print('rock stop:', self.height, self.min_ys, len(self.pts), self.max_min_y, rock)

        self.rocks += 1
        self.pts = self.pts.union(rock.pts)
        self.pts = self.clear_debris()
        return puffs

    def clear_debris(self):
        # keep only pts above (i.e. y is smaller than) lowest high y (max_min_y)
        before = len(self.pts)
        surface_pts = set([(x, y) for x, y in self.pts if y <= self.max_min_y])
        return surface_pts

    @property
    def height(self):
        # Remember ys increase as you go down and floor is 0
        return abs(min(self.min_ys))

    @property
    def min_ys(self):
        min_ys = [self.bottom_y] * self.width
        for x in range(self.width):
            rys = [ry for rx, ry in self.pts if rx == x]
            min_ys[x] = min(rys) if rys else self.bottom_y
        return min_ys

    @property
    def max_min_y(self):
        return max(self.min_ys)



    def __repr__(self):
        return f"<Chamber height={self.height} rocks={self.rocks}>"


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
        assert height == 3068, chamber
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
        print('est time:', est_secs, est_days, est_years)
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
        types = ROCK_TYPES.split('\n\n')
        rock = Rock(types[1], ROCK_SYMBOLS[1])
        assert rock.pt == (0, 0), rock
        assert rock.symbol == '+', rock
        assert rock.height == 3, rock
        assert rock.width == 3, rock
        assert len(rock.pts) == 5, rock
        print('test_rock passed')

    def test_chamber(self):
        chamber = TetrisChamber(7, TEST_INPUT)
        assert chamber.rock_types[0] == ('####', '—'), chamber.rock_types
        print('test_chamber passed')

    def test_drop(self):
        expected_rocks_pts = [
            (2, 1), (2, 2), (0, 4), (4, 4), (4, 8),
            (1, 10), (1, 11), (3, 13), (4, 14), (0, 13)
        ]

        chamber = TetrisChamber(7, TEST_INPUT)
        height = chamber.drop_rocks(len(expected_rocks_pts))

        for n, expected_pt in enumerate(expected_rocks_pts):
            rock = chamber.rocks[n]
            assert rock.pt == expected_pt, (n+1, expected_pt, rock)

        assert height == 17, (chamber, chamber.rocks, chamber.pts)
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
