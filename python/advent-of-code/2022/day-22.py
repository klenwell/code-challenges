"""
Advent of Code 2022 - Day 22
https://adventofcode.com/2022/day/22
"""
from os.path import join as path_join
from functools import cached_property
from config import INPUT_DIR


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
    def __init__(self, input):
        self.input = input

    @cached_property
    def board_map(self):
        map_input, _ = self.input.split("\n\n")
        return MonkeyMap(map_input)

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
        in_move = False

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
            print(self.board_map)

        # Facing is 0 for right (>), 1 for down (v), 2 for left (<), and 3 for up (^).
        # The final password is the sum of 1000 times the row, 4 times the column, and the facing.
        face_map = ['>', 'v', '<', '^']
        rowx1000 = self.board_map.row * 1000
        colx4 = self.board_map.col * 4
        facing = face_map.index(self.board_map.facing)
        return rowx1000 + colx4 + facing


class MonkeyMap:
    def __init__(self, input):
        self.input = input
        self.pt = self.starting_pt
        self.facing = '>'

    @property
    def col(self):
        return self.pt[0] + 1

    @property
    def row(self):
        return self.pt[1] + 1

    @cached_property
    def tiles(self):
        tiles = {}
        for y, row in enumerate(self.rows):
            for x, tile in enumerate(row):
                tiles[(x, y)] = tile
        return tiles

    @cached_property
    def pts(self):
        return list(self.tiles.keys())

    @cached_property
    def rows(self):
        rows =[]
        for line in self.input.split('\n'):
            row = list(line)
            rows.append(row)
        return rows

    @cached_property
    def starting_pt(self):
        x = next(n for n, x in enumerate(self.rows[0]) if x == '.')
        y = 0
        return (x, y)

    def move(self, movement):
        print('move', self, movement)
        rotation, tiles = movement
        self.facing = self.rotate(self.facing, rotation)
        self.pt = self.go(tiles)
        return self.pt

    def go(self, tiles):
        steps = {
            '>': (1, 0),
            'v': (0, 1),
            '<': (-1, 0),
            '^': (0, -1)
        }

        step = steps[self.facing]

        for n in range(tiles):
            x, y = self.pt
            dx, dy = step
            nx, ny = x+dx, y+dy
            next_tile = self.tiles.get((nx, ny))

            if next_tile is None or next_tile == ' ':
                (nx, ny) = self.wrap_around(self.facing, self.pt)
                next_tile = self.tiles.get((nx, ny))

            if next_tile == '.':
                self.pt = (nx, ny)
            elif next_tile == '#':
                self.pt = (x, y)
                return self.pt
            else:
                raise Exception('Unexpected tile:', tile)

        return self.pt

    def wrap_around(self, facing, pt):
        # If a movement instruction would take you off of the map, you wrap around to the other
        # side of the board. In other words, if your next tile is off of the board, you should
        # instead look in the direction opposite of your current facing as far as you can until
        # you find the opposite edge of the board, then reappear there.
        valid_tiles = ('.', '#')

        if facing == '>':
            row_pts = [pt for pt in self.pts if pt[1] == self.pt[1] and self.tiles[pt] in valid_tiles]
            next_pt = sorted(row_pts, key=lambda pt: pt[0])[0]
        elif facing == '<':
            row_pts = [pt for pt in self.pts if pt[1] == self.pt[1] and self.tiles[pt] in valid_tiles]
            next_pt = sorted(row_pts, key=lambda pt: pt[0])[-1]
        elif facing == '^':
            col_pts = [pt for pt in self.pts if pt[0] == self.pt[0] and self.tiles[pt] in valid_tiles]
            next_pt = sorted(col_pts, key=lambda pt: pt[0])[-1]
        else:  # == 'v'
            col_pts = [pt for pt in self.pts if pt[0] == self.pt[0] and self.tiles[pt] in valid_tiles]
            next_pt = sorted(col_pts, key=lambda pt: pt[0])[0]

        return next_pt

    def rotate(self, facing, rotation):
        seqs = {
            'L': '>^<v',
            'R': '>v<^'
        }

        seq = seqs.get(rotation)

        if not seq:
            return facing

        # Rotate to current spot
        q = list(seq)
        dir = q.pop(0)
        while dir != facing:
            q.append(dir)
            dir = q.pop(0)

        # New facing direction will be next in queue
        return q[0]


    def __repr__(self):
        return f"<MonkeyMap pt={self.pt} facing=({self.facing})>"


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

        # Act / Assert
        assert decoder.board_map.col == 8, decoder.board_map.col
        assert decoder.board_map.row == 6, decoder.board_map.row
        assert password == 6032, password
        return password

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

    @property
    def first(self):
        input = self.input_lines
        return input

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
            return file.read()

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
print(f"test 1 solution: {solution.test1}")
print(f"pt 1 solution: {solution.first}")
print(f"test 2 solution: {solution.test2}")
print(f"pt 2 solution: {solution.second}")
