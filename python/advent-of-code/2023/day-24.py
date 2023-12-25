"""
Advent of Code 2023 - Day 24
https://adventofcode.com/2023/day/24
"""
from os.path import join as path_join
from functools import cached_property
from common import INPUT_DIR, info


class HailCollider:
    def __init__(self, input, lo_bound, hi_bound):
        self.input = input.strip()
        self.lo_bound = lo_bound
        self.hi_bound = hi_bound

    @cached_property
    def xy_intersections(self):
        intersections = 0
        tested = set()
        for n, stone in enumerate(self.stones):
            info(f"checking stone {n}", 1)
            for o, other in enumerate(self.stones):
                id = tuple(sorted([n, o]))
                if id in tested:
                    continue
                tested.add(id)
                if stone.intersects_in_range(other, self.lo_bound, self.hi_bound ):
                    intersections += 1
        return intersections

    @cached_property
    def stones(self):
        stones = []
        for line in self.input.split('\n'):
            left, right = line.split(' @ ')
            pt = [int(n.strip()) for n in left.split(', ')]
            v = [int(n.strip()) for n in right.split(', ')]
            stone = HailStone(pt, v)
            stones.append(stone)
        return stones


class HailStone:
    class ParallelLines(Exception): pass

    def __init__(self, pt, v):
        self.pt = tuple(pt)
        self.v = tuple(v)

    @property
    def line(self):
        # https://stackoverflow.com/a/20679579/1093087
        p1 = self.pt
        p2 = (self.pt[0] + self.v[0], self.pt[1] + self.v[1])
        A = (p1[1] - p2[1])
        B = (p2[0] - p1[0])
        C = (p1[0]*p2[1] - p2[0]*p1[1])
        return A, B, -C

    def intersection(self, other):
        # https://stackoverflow.com/a/20679579/1093087
        L1 = self.line
        L2 = other.line
        D  = L1[0] * L2[1] - L1[1] * L2[0]
        Dx = L1[2] * L2[1] - L1[1] * L2[2]
        Dy = L1[0] * L2[2] - L1[2] * L2[0]
        if D != 0:
            x = Dx / D
            y = Dy / D
            return x, y
        else:
            raise HailStone.ParallelLines()

    def intersects_in_range(self, other, lo_bound, hi_bound):
        try:
            x, y = self.intersection(other)
            if x < lo_bound or x > hi_bound:
                return False
            if y < lo_bound or y > hi_bound:
                return False
            #print('x', (x, y), (lo_bound, hi_bound))
            return self.xy_in_future(x, y) and other.xy_in_future(x, y)
        except HailStone.ParallelLines:
            return False

    def xy_in_future(self, x, y):
        dvx = self.v[0] > 0
        dvy = self.v[1] > 0
        dx = (x - self.pt[0]) > 0
        dy = (y - self.pt[1]) > 0
        return dvx == dx and dvy == dy

    def __repr__(self):
        return f"<Hail pt={self.pt} v={self.v}>"


class AdventPuzzle:
    INPUT_FILE = path_join(INPUT_DIR, 'day-24.txt')

    TEST_INPUT = """\
19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3"""

    #
    # Solutions
    #
    @property
    def first(self):
        input = self.file_input
        low_bound, high_bound = 200000000000000, 400000000000000
        collider = HailCollider(input, low_bound, high_bound)
        return collider.xy_intersections

    @property
    def second(self):
        pass

    #
    # Tests
    #
    @property
    def test1(self):
        h1 = HailStone((19, 13), (-2, 1))
        h2 = HailStone((18, 19), (-1, -1))
        ix, iy = h1.intersection(h2)
        assert round(ix, 2) == 14.33, ix
        assert round(iy, 2) == 15.33, iy

        h1 = HailStone((18, 19, 22), (-1, -1, 2))
        h2 = HailStone((20, 19, 15), (1, -5, -3))
        ix, iy = h1.intersection(h2)
        assert h1.xy_in_future(ix, iy) == False
        assert h2.xy_in_future(ix, iy) == False

        input = self.TEST_INPUT
        low_bound, high_bound = 7, 27
        collider = HailCollider(input, low_bound, high_bound)
        assert collider.xy_intersections == 2, collider.xy_intersections

        return 'passed'

    @property
    def test2(self):
        input = self.TEST_INPUT
        print(input)
        return 'passed'

    #
    # Etc...
    #
    @cached_property
    def file_input(self):
        with open(self.INPUT_FILE) as file:
            return file.read().strip()

    def solve(self):
        print(f"test 1 solution: {self.test1}")
        print(f"Part 1 Solution: {self.first}")
        print(f"test 2 solution: {self.test2}")
        print(f"Part 2 Solution: {self.second}")


#
# Main
#
puzzle = AdventPuzzle()
puzzle.solve()
