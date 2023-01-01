"""
Advent of Code 2022 - Day 17
https://adventofcode.com/2022/day/17
"""
from os.path import join as path_join
from functools import cached_property
from config import INPUT_DIR


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
        for y, row in enumerate(self.rows):
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
        self.start_y = -3

    def drop_rocks(self, num):
        for n in range(num):
            type, symbol = self.rock_types[n % len(self.rock_types)]
            rock = Rock(type, symbol)

            print('drop rock', n+1)
            self.drop_rock(rock)

        return self.height

    def drop_rock(self, rock):
        rock.x = self.start_x
        rock.y = self.bottom_y - self.height - rock.height + self.start_y
        dropping = True

        print('rock start:', rock)
        while dropping:
            rock = self.jet_push_rock(rock)
            rock.y += 1
            collision = rock.overlaps(self) or self.rock_hits_floor(rock)

            if collision:
                rock.y -= 1  # restore to previous point
                break
            print('dropping:', rock)
        print('rock stop:', rock)

        self.pts = self.pts.union(rock.pts)
        self.rocks.append(rock)

    def jet_push_rock(self, rock):
        init_x = rock.x

        puff = self.jet_queue.pop(0)
        rock.x += PUFF_OFFSET[puff]
        self.jet_queue.append(puff)
        print(init_x, puff, PUFF_OFFSET[puff], rock.x)

        # If hits wall or resting rock, restore x
        if self.rock_hits_wall(rock) or rock.overlaps(self):
            print('wall')
            rock.x = init_x

        return rock

    def rock_hits_wall(self, rock):
        return rock.x < 0 or rock.max_x > self.width

    def rock_hits_floor(self, rock):
        return rock.y >= self.bottom_y

    @property
    def height(self):
        if not self.rocks:
            return self.bottom_y
        return abs(min(rock.y for rock in self.rocks))

    def __repr__(self):
        return f"<Chamber height={self.height} rocks={len(self.rocks)}>"



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
        pass

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
            (2, -1), (2, -4), (0, -6), (4, -7), (4, -9),
            (1, -10), (1, -13), (3, -15), (4, -17), (0, -14)
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
