"""
Advent of Code 2022 - Day 22 - Monkey Map
https://adventofcode.com/2022/day/22
"""
from os.path import join as path_join
from functools import cached_property
from config import INPUT_DIR

from models.monkey_map.grove_map import GroveMap
from models.monkey_map.test_cube_map import TestCubeMap


INPUT_FILE = path_join(INPUT_DIR, 'day-22.txt')

TEST_INPUT = """\
        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5"""


class PasswordDecoder:
    def __init__(self, input, map_class=None):
        self.input = input
        self.map_class = map_class if map_class else GroveMap

    @cached_property
    def board_map(self):
        map_input, _ = self.input.split("\n\n")
        return self.map_class(map_input)

    @cached_property
    def path_code(self):
        _, path_input = self.input.split("\n\n")
        return path_input.strip()

    @property
    def movements(self):
        moves = []
        path_code = f"N{self.path_code}"
        rotate = None
        tiles = []

        for char in list(path_code):
            if char.isalpha():
                if rotate:
                    next_move = (rotate, int(''.join(tiles)))
                    moves.append(next_move)
                    tiles = []
                rotate = char
            else:
                tiles.append(char)

        next_move = (rotate, int(''.join(tiles)))
        moves.append(next_move)
        return moves

    @property
    def password(self):
        return self.decode_password()

    def decode_password(self):
        for move in self.movements:
            self.board_map.move(move)

        # Facing is 0 for right (>), 1 for down (v), 2 for left (<), and 3 for up (^).
        # The final password is the sum of 1000 times the row, 4 times the column, and the facing.
        face_map = ['>', 'v', '<', '^']
        rowx1000 = self.board_map.row * 1000
        colx4 = self.board_map.col * 4
        facing = face_map.index(self.board_map.facing)
        return rowx1000 + colx4 + facing


class GroveCubeMap(TestCubeMap):
    @cached_property
    def edges(self):
        return {
            # ID: (x(s), y(s))
            '1^': ((100, 150), 0),
            '1>': (149, (0, 50)),
            '1v': ((100, 150), 49),
            '2^': ((50, 100), 0),
            '2<': (50, (0, 50)),
            '3>': (99, (50, 100)),
            '3<': (50, (50, 100)),
            '4>': (99, (100, 150)),
            '4v': ((50, 100), 149),
            '5^': ((0, 50), 100),
            '5<': (0, (100, 150)),
            '6>': (49, (150, 200)),
            '6v': ((0, 50), 199),
            '6<': (0, (150, 200))
        }

    @cached_property
    def hinges(self):
        return (
            # edge1, edge2, twist?
            ('1^', '6v', False),
            ('1>', '4>', True),
            ('1v', '3>', False),
            ('2^', '6<', False),
            ('2<', '5<', True),
            ('3<', '5^', False),
            ('4v', '6>', False)
        )

    @cached_property
    def step_delta(self):
        return {
            '>': (1, 0),
            'v': (0, 1),
            '<': (-1, 0),
            '^': (0, -1)
        }

    @cached_property
    def hinge_pts(self):
        # Map (x, y, dir) to (x, y, dir) where two open edges connect
        pts = {}

        for edge1_id, edge2_id, twist in self.hinges:
            edge1_pts = self.edges[edge1_id]
            edge2_pts = self.edges[edge2_id]
            edge1 = Edge(edge1_id, edge1_pts)
            edge2 = Edge(edge2_id, edge2_pts)

            hinge = Hinge(edge1, edge2, twist)

            for footprint1, footprint2 in hinge.paired_footprints:
                pts[footprint1] = footprint2

        return pts

    def cross_hinge(self, facing, pt):
        x, y = pt
        footprint = (x, y, facing)
        return self.hinge_pts[footprint]

    def go(self, tiles):
        for n in range(tiles):
            x, y = self.pt
            dx, dy = self.step_delta[self.facing]
            nx, ny = x+dx, y+dy
            facing = self.facing
            next_tile = self.tiles.get((nx, ny))

            if next_tile not in ('.', '#'):
                (nx, ny, facing) = self.cross_hinge(self.facing, self.pt)
                next_tile = self.tiles.get((nx, ny))

            if next_tile == '.':
                self.pt = (nx, ny)
                self.facing = facing
                self.footprints.append((self.footprint, next_tile))
            elif next_tile == '#':
                self.pt = (x, y)
                self.footprints.append((self.footprint, next_tile))
                return self.pt  # Hit a wall: stop and return
            else:
                breakpoint()
                raise Exception('Unexpected tile:', self.pt, (nx, ny), next_tile)

        return self.pt


class Edge:
    def __init__(self, id, pts):
        xs, ys = pts
        self.id = id
        self.facing = id[1]
        self.xs = xs
        self.ys = ys

    @cached_property
    def long_axis(self):
        return 'x' if type(self.xs) == tuple else 'y'

    @cached_property
    def pts(self):
        pts = []
        ranger = self.xs if self.long_axis == 'x' else self.ys
        for n in range(*ranger):
            x = n if self.long_axis == 'x' else self.xs
            y = n if self.long_axis == 'y' else self.ys
            pt = (x, y)
            pts.append(pt)
        return pts

    @cached_property
    def footprints(self):
        footprints = []
        for pt in self.pts:
            x, y = pt
            footprint = (x, y, self.facing)
            footprints.append(footprint)
        return footprints


class Hinge:
    def __init__(self, edge1, edge2, twist):
        self.edge1 = edge1
        self.edge2 = edge2
        self.twisted = twist

    @cached_property
    def paired_footprints(self):
        pairs = []

        if self.twisted:
            next_footprints = list(reversed(self.edge2.footprints))
        else:
            next_footprints = list(self.edge2.footprints)

        for n, footprint1 in enumerate(self.edge1.footprints):
            footprint2 = next_footprints[n]
            x1, y1, facing1 = footprint1
            x2, y2, facing2 = footprint2
            pair1 = (footprint1, (x2, y2, self.about_face(facing2)))
            pair2 = (footprint2, (x1, y1, self.about_face(facing1)))
            pairs.append(pair1)
            pairs.append(pair2)

        return pairs

    def about_face(self, facing):
        mapped = {
            '^': 'v',
            '>': '<',
            'v': '^',
            '<': '>'
        }

        return mapped[facing]


class Solution:
    def __init__(self, input_file):
        self.input_file = input_file

    #
    # Solutions
    #
    @property
    def test1(self):
        # Arrange
        input = TEST_INPUT
        decoder = PasswordDecoder(input)

        # Assume
        self.test_decoder()
        self.test_rotation()

        # Act
        password = decoder.password

        # Assert
        assert decoder.board_map.col == 8, decoder.board_map.col
        assert decoder.board_map.row == 6, decoder.board_map.row
        assert password == 6032, password
        return password

    @property
    def first(self):
        input = self.file_input
        decoder = PasswordDecoder(input)
        password = decoder.password

        assert password != 144282, "Too high"
        assert password != 61054, "Too low"
        return password

    @property
    def test2(self):
        # Arrange
        input = TEST_INPUT
        decoder = PasswordDecoder(input, map_class=TestCubeMap)

        # Act
        password = decoder.password

        # Assert
        assert decoder.board_map.col == 7, decoder.board_map.col
        assert decoder.board_map.row == 5, decoder.board_map.row
        assert password == 5031, password
        return password

    @property
    def second(self):
        input = self.file_input
        decoder = PasswordDecoder(input, map_class=GroveCubeMap)
        password = decoder.password
        assert password == 162038, password
        return password

    #
    # Tests
    #
    def test_decoder(self):
        input = TEST_INPUT
        decoder = PasswordDecoder(input)

        expected_moves = [('N', 10), ('R', 5), ('L', 5), ('R', 10), ('L', 4), ('R', 5), ('L', 5)]
        assert decoder.path_code == '10R5L5R10L4R5L5', decoder.path_code
        assert decoder.movements == expected_moves, decoder.movements
        assert decoder.board_map.starting_pt == (8, 0), decoder.board_map
        assert decoder.board_map.facing == '>', decoder.board_map

        print('+ test_decoder passed')

    def test_rotation(self):
        input = TEST_INPUT
        decoder = PasswordDecoder(input)
        monkey_map = decoder.board_map

        cases = [
            # facing, rotate, expect
            ('>', 'L', '^'),
            ('>', 'R', 'v'),
            ('^', 'L', '<'),
            ('v', 'R', '<'),
            ('v', 'L', '>'),
            ('<', 'L', 'v'),
            ('<', 'R', '^'),
            ('^', 'R', '>'),
            ('^', 'L', '<'),
            ('>', 'N', '>')
        ]

        for facing, rotation, expected in cases:
            assert monkey_map.rotate(facing, rotation) == expected, (facing, rotation, expected)

        print('+ test_rotation passed')

    #
    # Properties
    #
    @cached_property
    def file_input(self):
        with open(self.input_file) as file:
            return file.read()


#
# Main
#
solution = Solution(INPUT_FILE)
print(f"test 1 solution: {solution.test1}")
print(f"pt 1 solution: {solution.first}")
print(f"test 2 solution: {solution.test2}")
print(f"pt 2 solution: {solution.second}")
