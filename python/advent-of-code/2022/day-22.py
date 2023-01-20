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
    def __init__(self, input, map_class=None):
        self.input = input
        self.map_class = map_class if map_class else MonkeyMap

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
            #print(self.board_map)

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
        self.footprints = []

    @property
    def x(self):
        return self.pt[0]

    @property
    def y(self):
        return self.pt[1]

    @property
    def col(self):
        return self.x + 1

    @property
    def row(self):
        return self.y + 1

    @property
    def footprint(self):
        return (self.facing, self.pt)

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
    def tiled_pts(self):
        return [pt for pt in self.pts if self.tiles[pt] in ('.', '#')]

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
        start_pt = str(self)
        rotation, tiles = movement
        self.facing = self.rotate(self.facing, rotation)
        self.pt = self.go(tiles)
        print('move', start_pt, movement, self)
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

            if next_tile not in ('.', '#'):
                (nx, ny) = self.wrap_around(self.facing, self.pt)
                next_tile = self.tiles.get((nx, ny))

            if next_tile == '.':
                self.pt = (nx, ny)
                self.footprints.append((self.footprint, next_tile))
            elif next_tile == '#':
                self.pt = (x, y)
                self.footprints.append((self.footprint, next_tile))
                return self.pt  # Hit a wall: stop and return
            else:
                raise Exception('Unexpected tile:', self.pt, (nx, ny), next_tile)

        return self.pt

    def wrap_around(self, facing, pt):
        # If a movement instruction would take you off of the map, you wrap around to the other
        # side of the board. In other words, if your next tile is off of the board, you should
        # instead look in the direction opposite of your current facing as far as you can until
        # you find the opposite edge of the board, then reappear there.
        valid_tiles = ('.', '#')
        x, y = pt

        if facing == '>':
            # Go left until you hit a break
            nx = x
            while True:
                nx -= 1
                if (nx, y) not in self.tiled_pts:
                    next_pt = (nx+1, y)
                    break
        elif facing == '<':
            # Go right until you hit a break
            nx = x
            while True:
                nx += 1
                if (nx, y) not in self.tiled_pts:
                    next_pt = (nx-1, y)
                    break
        elif facing == '^':
            # Go down until you hit a break
            ny = y
            while True:
                ny += 1
                if (x, ny) not in self.tiled_pts:
                    next_pt = (x, ny-1)
                    break
        else:  # == 'v'
            # Go up until you hit a break
            ny = y
            while True:
                ny -= 1
                if (x, ny) not in self.tiled_pts:
                    next_pt = (x, ny+1)
                    break

        print(f"{pt} facing {facing} wraps to {next_pt}")
        #breakpoint()
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
        print(f'rotate {rotation} from {facing} to {q[0]}')
        return q[0]

    def __repr__(self):
        return f"<MonkeyMap pt={self.pt} facing=({self.facing})>"


class TestCubeMap(MonkeyMap):
    def map_edges(self, edge1, edge2):
        return dict(zip(range(*edge1), range(*edge2)))

    def wrap_around(self, facing, pt):
        x, y = pt

        # Side 1^ to 2^
        if y == 0 and facing == '^':
            x_map = self.map_edges((8, 11), (3, -1, -1))
            nx = x_map[x]
            ny = 4
            nf = 'v'

        # Side 1< to 3^
        elif x == 7 and y in range(0, 4) and facing == '<':
            yx_map = self.map_edges((0, 4), (4, 8))
            nx = yx_map[y]
            ny = 4
            nf = 'v'

        # Side 1> to 6>
        elif x == 11 and y in range(0, 4) and facing == '>':
            y_map = self.map_edges((0, 4), (11, 7, -1))
            nx = 15
            ny = y_map[y]
            nf = '<'

        # Side 2^ to 1^
        elif y == 4 and x in range(0, 4) and facing == '^':
            x_map = self.map_edges((0, 4), (3, -1, -1))
            nx = x_map[x]
            ny = 0
            nf = 'v'

        # Side 2< to 6v
        elif x == 0 and y in range(4, 8) and facing == '<':
            yx_map = self.map_edges((4, 8), (15, 11, -1))
            nx = yx_map[x]
            ny = 11
            nf = '^'

        # Side 2v to 5v
        elif y == 7 and x in range(0, 4) and facing == 'v':
            print('Side 2v to 5v')
            yx_map = self.map_edges((0, 4), (11, 7, -1))
            nx = yx_map[x]
            ny = 11
            nf = '^'

        # Side 3^ to 1<
        elif y == 4 and x in range(4, 8) and facing == '^':
            xy_map = self.map_edges((4, 8), (0, 4))
            nx = 8
            ny = xy_map[x]
            nf = '>'

        # Side 3v to 5<
        elif y == 7 and x in range(4, 8) and facing == 'v':
            xy_map = self.map_edges((4, 8), (11, 7, -1))
            nx = 8
            ny = xy_map[x]
            nf = '>'

        # Side 4> to 6^
        elif x == 11 and y in range(4, 8) and facing == '>':
            yx_map = self.map_edges((4, 8), (15, 11, -1))
            nx = yx_map[y]
            ny = 8
            nf = 'v'

        # Side 5< to 3v
        elif x == 8 and y in range(8, 12) and facing == '<':
            yx_map = self.map_edges((8, 12), (7, 3, -1))
            nx = yx_map[x]
            ny = 7
            nf = '^'

        # Side 5v to 2v
        elif y == 11 and x in range(8, 12) and facing == 'v':
            x_map = self.map_edges((8, 12), (3, -1, -1))
            nx = x_map[x]
            ny = 7
            nf = '^'

        # Side 6^ to 4>
        elif y == 8 and x in range(12, 16) and facing == '^':
            xy_map = self.map_edges((12, 16), (4, 8))
            nx = 11
            ny = xy_map[x]
            nf = '<'

        # Side 6> to 1>
        elif x == 15 and y in range(8, 12) and facing == '>':
            y_map = self.map_edges((8, 12), (3, -1, -1))
            nx = 11
            ny = y_map[y]
            nf = '<'

        # Side 6v to 2<
        elif y == 11 and x in range(12, 16) and facing == 'v':
            xy_map = self.map_edges((12, 16), (7, 3, -1))
            nx = 0
            ny = xy_map[x]
            nf = '>'

        else:
            breakpoint()
            raise Exception(f"Missed wrap case: {(facing, pt)}")

        print(f"{(x, y, facing)} wraps to {(nx, ny, nf)}")
        #breakpoint()
        return (nx, ny, nf)

    def go(self, tiles):
        steps = {
            '>': (1, 0),
            'v': (0, 1),
            '<': (-1, 0),
            '^': (0, -1)
        }

        for n in range(tiles):
            x, y = self.pt
            dx, dy = steps[self.facing]
            nx, ny = x+dx, y+dy
            facing = self.facing
            next_tile = self.tiles.get((nx, ny))

            if next_tile not in ('.', '#'):
                print(f"pt {(self.facing, self.pt)} not a tile: {next_tile} {n}")
                (nx, ny, facing) = self.wrap_around(self.facing, self.pt)
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


class CubeMap(TestCubeMap):
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
        #breakpoint()
        x, y = pt
        footprint = (x, y, facing)
        return self.hinge_pts[footprint]

    def go(self, tiles):
        for n in range(tiles):
            x, y = self.pt
            print(self.facing)
            dx, dy = self.step_delta[self.facing]
            nx, ny = x+dx, y+dy
            facing = self.facing
            next_tile = self.tiles.get((nx, ny))

            if next_tile not in ('.', '#'):
                print(f"pt {(self.facing, self.pt)} not a tile: {next_tile} {n}")
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

        #breakpoint()
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
        decoder = PasswordDecoder(input, map_class=CubeMap)
        password = decoder.password
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
#print(f"test 1 solution: {solution.test1}")
#print(f"pt 1 solution: {solution.first}")
print(f"test 2 solution: {solution.test2}")
print(f"pt 2 solution: {solution.second}")
